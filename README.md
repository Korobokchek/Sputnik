## Спецификация языка SSYP_0

### Описание языка
SSYP_0 - это простой язык программирования, который используется для обучения основам программирования. Он имеет небольшой набор команд и поддерживает только целочисленные вычисления. 
Алфавит SSYP_0 включает 60 символов: $ @ # A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 = + — * / () , . ' % ; : ¬ & | > < _ ?.

Язык SSYP_0 требует, чтобы была хотя бы одна переменная.

### Операторы
Все действия в SSYP_0 начинаются с символа "#", после чего пишется определенное действие.

- Оператор присваивания "=" присваивает значение выражения переменной. Пример: "#= y #42".
- Условный оператор "if" выполняет блок операторов, если условие истинно.
- Условный оператор "else" выполняет блок операторов, если условие ложно.
- Блок операторов "F_BEGIN" и "F_END" позволяет сделать функцию.

### Переменные
- Переменные обозначаются символом "@", после чего прописывается тип переменной (возможен только тип "INT"), а затем пишется название переменной. 
- Они могут содержать только целочисленные значения.

### Выражения
SSYP_0 поддерживает следующие выражения:
- Арифметические операции: "+", "-", "*", "/".
- Операции сравнения: "=", "<>", "<", ">", "<=", ">=".
- После символа "#" и операции пишутся три аргумента: первый - куда записывается результат операции, второй - первое значение операции, третий - второе значение операции.

### Функции
- "Print" используется для вывода информации в терминал.

### Пример программы
1.#F_BEGIN;
1. #F_NAME name;
1. #F_ARGS_BEGIN;
1.   @INT z;
1.   @INT q;
1. #F_ARGS_END;
1. #F_VARS_BEGIN;
1.  @INT x;
1.  @INT y;
1. #F_VARS_END;
1. #F_BODY_BEGIN;
1.  #+ x y z;
1.  #* q x y;
1. #F_RETURN;
1.#F_BODY_END;
1.#F_END# name x y


### Процедуры

### Примеры программ

## Спецификация ByteCode

- ADD dst src1 src2: сложение. Первый параметр - куда складывать значение на стек, второй - место на стеке, откуда взять первый параметр действия, третий - место второго параметра.
- SUB dst src1 src2: вычитание. Первый параметр - куда складывать значение на стек, второй - место на стеке, откуда взять первый параметр действия, третий - место второго параметра.
- MUL dst src1 src2: умножение. Первый параметр - куда складывать значение на стек, второй - место на стеке, откуда взять первый параметр действия, третий - место второго параметра.
- DIV dst src1 src2: деление. Первый параметр - куда складывать значение на стек, второй - место на стеке, откуда взять первый параметр действия, третий - место второго параметра.
- SET dst_off number: установка значения. Первый параметр - смещение на стеке, второй - число.
- RETURN name off: вызов функции с возвратом. Первый параметр - имя функции, второй - смещение на стеке.
- MOV dst_off src_offJMP cmp_type jump_off: переход. Первый параметр - смещение назначения, второй - смещение источника, третий - тип сравнения, четвертый - смещение перехода.

