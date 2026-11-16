
package in.ps024.gst.io;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class CommandFileReader {

    public record Command(
            int lineNumber,
            String name,
            List<String> arguments,
            String rawLine
    ) {}

    public List<Command> read(Path filePath) throws IOException {

        List<String> lines =
                Files.readAllLines(filePath, StandardCharsets.UTF_8);

        List<Command> commands = new ArrayList<>();

        for (int i = 0; i < lines.size(); i++) {

            String line = lines.get(i).strip();

            // Remove UTF-8 BOM if present on the first line
            if (i == 0 && line.startsWith("\uFEFF")) {
                line = line.substring(1);
            }

            // Ignore blank lines and comments
            if (line.isEmpty() || line.startsWith("#")) {
                continue;
            }

            // Split command using | separator
            String[] parts = line.split("\\|", -1);

            String commandName =
                    parts[0].strip().toUpperCase(Locale.ROOT);

            List<String> arguments = new ArrayList<>();

            for (int j = 1; j < parts.length; j++) {
                arguments.add(parts[j].strip());
            }

            commands.add(new Command(
                    i + 1,
                    commandName,
                    List.copyOf(arguments),
                    line
            ));
        }

        return commands;
    }
}

