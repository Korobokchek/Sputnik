import Parsing.Function;
import Parsing.Instruction;
import Parsing.InstructionType;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

class VmTranslating {
    public static String translate(Function[] functions) {
        StringBuilder byteCode = new StringBuilder();
        for(Function func : functions) {
            byteCode.append(generateFunction(func));
            byteCode.append("\n");

        }

        return byteCode.toString();
    }

    private static String generateFunction(Function func) {
        ArrayList<String> virtualStack = new ArrayList<>();
        StringBuilder byteCode = new StringBuilder();
        virtualStack.addAll(Arrays.stream(func.arguments).map(arg -> arg.name).collect(Collectors.toSet()));
        virtualStack.addAll(Arrays.stream(func.locals).map(arg -> arg.name).collect(Collectors.toSet()));


        for(Instruction instruction : func.instructions) {
            switch (instruction.type()) {
                case ADD:

                    if ( instruction.get(0).isPresent() ) {
                        instruction.get(0).get();
                    }
                    else {
                        System.out.println("Error ");
                        throw new RuntimeException();
                    }
                    if ( instruction.get(1).isPresent() ) {
                        instruction.get(1).get();
                    }
                    else {
                        System.out.println("Error");
                        throw new RuntimeException();
                    }
                    if ( instruction.get(2).isPresent() ) {
                        instruction.get(2).get();
                    }
                    else {
                        System.out.println("Error");
                        throw new RuntimeException();
                    }

//                    byteCode.append(String.format("ADD %d %d %d", ));
                    break;
            }
        }

        return "";
    }
}

