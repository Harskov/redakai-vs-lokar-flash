import java.io.IOException;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.Instrumentation;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.ProtectionDomain;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Stream;

/**
 * A Java agent that gives a class the bytes of the compiled class file of the same name under the folder named as the
 * agent's argument, as the class is loaded: FFDec's jars stay as released (they are signed, so a class of the same
 * package placed earlier on the class path is refused), and the patched class is defined from the jar it belongs to.
 * Every overlay file is read before the program starts, so an unreadable one stops the JVM instead of leaving the
 * released class in place.
 */
public final class ClassOverlayAgent implements ClassFileTransformer {

    private final Map<String, byte[]> overlay;

    private ClassOverlayAgent(Map<String, byte[]> overlay) {
        this.overlay = overlay;
    }

    public static void premain(String args, Instrumentation inst) throws IOException {
        Path root = Paths.get(args);
        Map<String, byte[]> overlay = new HashMap<>();
        try (Stream<Path> files = Files.walk(root)) {
            for (Path p : (Iterable<Path>) files::iterator) {
                String rel = root.relativize(p).toString().replace('\\', '/');
                if (rel.endsWith(".class")) {
                    overlay.put(rel.substring(0, rel.length() - 6), Files.readAllBytes(p));
                }
            }
        }
        if (overlay.isEmpty()) {
            throw new IOException("no class file under " + root);
        }
        inst.addTransformer(new ClassOverlayAgent(overlay));
    }

    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> redefined, ProtectionDomain domain, byte[] bytes) {
        return className == null ? null : overlay.get(className);
    }
}
