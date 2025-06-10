% Выполнил студент группы 321701:
% - Мотолянец Кирилл Андреевич
% Вариант 11
%
% Решение для игры в пятнашки
% 05.06.2025
%
% Источники:
% - Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.

% print_board(+Board)
% Печатает текущее состояние доски 3x3.
print_board(Board) :-
    format('~`-t~13|~n'), % Горизонтальная линия
    nth0(0, Board, T0), nth0(1, Board, T1), nth0(2, Board, T2),
    format('| ~w | ~w | ~w |~n', [T0, T1, T2]),
    format('~`-t~13|~n'),
    nth0(3, Board, T3), nth0(4, Board, T4), nth0(5, Board, T5),
    format('| ~w | ~w | ~w |~n', [T3, T4, T5]),
    format('~`-t~13|~n'),
    nth0(6, Board, T6), nth0(7, Board, T7), nth0(8, Board, T8),
    format('| ~w | ~w | ~w |~n', [T6, T7, T8]),
    format('~`-t~13|~n').

% find_empty_spot(+Board, -Index)
% Находит индекс пустого места (0) на доске.
find_empty_spot(Board, Index) :-
    nth0(Index, Board, 0).

% swap_elements(+List, +Index1, +Index2, -NewList)
% Меняет местами элементы по заданным индексам в списке.
swap_elements(List, Index1, Index2, NewList) :-
    nth0(Index1, List, Val1),
    nth0(Index2, List, Val2),
    replace_nth0(Index1, Val2, List, TempList),
    replace_nth0(Index2, Val1, TempList, NewList).

% replace_nth0(+Index, +NewVal, +List, -NewList)
% Вспомогательный предикат для замены элемента по индексу.
replace_nth0(0, NewVal, [_|T], [NewVal|T]).
replace_nth0(N, NewVal, [H|T], [H|Rest]) :-
    N > 0,
    N1 is N - 1,
    replace_nth0(N1, NewVal, T, Rest).

% get_possible_moves(+Board, -NextBoard)
% Определяет возможное следующее состояние доски, перемещая плитку.
get_possible_moves(Board, NextBoard) :-
    find_empty_spot(Board, EmptyIdx),
    Row is EmptyIdx // 3,
    Col is EmptyIdx mod 3,

    % Определяем потенциальные соседние позиции
    (   (NewRow is Row - 1, NewCol is Col) % Вверх
    ;   (NewRow is Row + 1, NewCol is Col) % Вниз
    ;   (NewRow is Row, NewCol is Col - 1) % Влево
    ;   (NewRow is Row, NewCol is Col + 1) % Вправо
    ),
    % Проверяем границы доски
    NewRow >= 0, NewRow < 3,
    NewCol >= 0, NewCol < 3,

    TileToMoveIdx is NewRow * 3 + NewCol,
    swap_elements(Board, EmptyIdx, TileToMoveIdx, NextBoard).


% count_inversions(+List, -Count)
% Подсчитывает количество инверсий в списке (без учета 0).
count_inversions([], 0).
count_inversions([H|T], Count) :-
    H \== 0, % Игнорируем 0
    findall(X, (member(X, T), X \== 0, X < H), LessThanH),
    length(LessThanH, CurrentInversions),
    count_inversions(T, RestInversions),
    Count is CurrentInversions + RestInversions.
count_inversions([0|T], Count) :- % Если первый элемент 0, пропускаем его
    count_inversions(T, Count).

% is_solvable(+Board)
% Проверяет, является ли заданная конфигурация доски разрешимой.
% Для 3x3 головоломки: разрешима, если количество инверсий четное.
is_solvable(Board) :-
    count_inversions(Board, Inversions),
    Inversions mod 2 =:= 0.

% solve_puzzle(+InitialState, +TargetState, -SolutionPath)
% Основной предикат для решения головоломки.
solve_puzzle(InitialState, TargetState, SolutionPath) :-
    % Проверяем разрешимость начального состояния
    (   is_solvable(InitialState)
    ->
        % Инициализируем очередь: [ (Состояние, [Путь_до_состояния]) ]
        Queue = [(InitialState, [InitialState])],
        % Инициализируем посещенные состояния
        Visited = [InitialState],
        % Запускаем BFS
        bfs(Queue, Visited, TargetState, SolutionPath)
    ;
        writeln("Начальное состояние неразрешимо. Решение невозможно."),
        fail % Провалить, если неразрешимо
    ).

% bfs(+Queue, +Visited, +TargetState, -SolutionPath)
% Рекурсивный предикат для поиска в ширину.
bfs([(CurrentBoard, Path)|_], _Visited, CurrentBoard, Path). % Базовый случай: нашли целевое состояние
bfs([(CurrentBoard, Path)|RestOfQueue], Visited, TargetState, SolutionPath) :-
    CurrentBoard \== TargetState, % Продолжаем, если не целевое
    findall(NextBoard, get_possible_moves(CurrentBoard, NextBoard), PossibleMoves), % Находим все возможные ходы

    % Отфильтровываем уже посещенные состояния и строим новые элементы очереди
    append_new_states(PossibleMoves, Path, Visited, NewQueueElements, NewVisited),

    % Добавляем новые элементы в конец очереди, обновляем посещенные
    append(RestOfQueue, NewQueueElements, UpdatedQueue),

    % Рекурсивный вызов с обновленной очередью и посещенными
    bfs(UpdatedQueue, NewVisited, TargetState, SolutionPath).

% append_new_states(+PossibleMoves, +CurrentPath, +Visited, -NewQueueElements, -NewVisited)
% Вспомогательный предикат для добавления новых, еще не посещенных состояний в очередь.
append_new_states([], _Path, Visited, [], Visited).
append_new_states([NextBoard|RestMoves], Path, Visited, [(NextBoard, NewPath)|NewQueueElements], FinalVisited) :-
    \+ member(NextBoard, Visited), % Если состояние НЕ было посещено
    append(Path, [NextBoard], NewPath),
    append(Visited, [NextBoard], UpdatedVisited),
    append_new_states(RestMoves, Path, UpdatedVisited, NewQueueElements, FinalVisited).
append_new_states([_NextBoard|RestMoves], Path, Visited, NewQueueElements, FinalVisited) :-
    member(_NextBoard, Visited), % Если состояние УЖЕ было посещено, пропускаем
    append_new_states(RestMoves, Path, Visited, NewQueueElements, FinalVisited).

% print_solution_path(+Path)
% Выводит пошаговое решение.
print_solution_path(Path) :-
    (   Path == []
    ->  writeln("Путь решения пуст.")
    ;   length(Path, Len),
        Steps is Len - 1,
        format("Найдено решение за ~w шагов:~n", [Steps]),
        print_steps(Path, 0)
    ).

% print_steps(+Path, +StepNum)
% Рекурсивный предикат для вывода каждого шага.
print_steps([], _).
print_steps([Board|Rest], StepNum) :-
    format("~nШаг ~w:~n", [StepNum]),
    print_board(Board),
    (   Rest == []
    ->  true
    ;   writeln("  ↓"),
        NextStepNum is StepNum + 1,
        print_steps(Rest, NextStepNum)
    ).

% --- Примеры использования ---

% Пример 1: Разрешимое состояние
initial_board_1([1, 2, 3, 4, 5, 6, 7, 0, 8]).
target_board_1([1, 2, 3, 4, 5, 6, 7, 8, 0]).

% Пример 2: Разрешимое состояние, требующее нескольких шагов
initial_board_2([1, 2, 3, 0, 4, 6, 7, 5, 8]).
target_board_2([1, 2, 3, 4, 5, 6, 7, 8, 0]).

% Пример 3: Неразрешимое состояние
initial_board_3([8, 1, 2, 0, 4, 3, 7, 6, 5]).
target_board_3([1, 2, 3, 4, 5, 6, 7, 8, 0]).

% Запуск:
% initial_board_1(I1), target_board_1(T1), solve_puzzle(I1, T1, Sol1), print_solution_path(Sol1).
% initial_board_2(I2), target_board_2(T2), solve_puzzle(I2, T2, Sol2), print_solution_path(Sol2).
% initial_board_3(I3), target_board_3(T3), solve_puzzle(I3, T3, Sol3), print_solution_path(Sol3).
