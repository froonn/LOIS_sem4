"""
Выполнил студент группы 321701:
- Мотолянец Кирилл Андреевич
Вариант 6

Классы для представления формул сокращенного языка логики высказываний в виде абстрактного синтаксического дерева (AST).
23.05.2025

Источники:
- Логические основы интеллектуальных систем. Практикум : учебно - метод. пособие / В. В. Голенков [и др.]. – Минск : БГУИР, 2011. – 70 с. : ил.
"""


class Expr:
    """
    Base class for all expressions in the logical formula.
    """

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the expression in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of evaluating the expression.
        """
        pass


class ConstTrue(Expr):
    """
    Class representing a constant logical value of True in a logical formula.
    """

    def __repr__(self):
        """
        Returns a string representation of the constant True.

        Returns:
            str: The string 'ConstTrue()'.
        """
        return 'ConstTrue()'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluates the constant True.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values (not used).

        Returns:
            bool: Always True.
        """
        return True


class ConstFalse(Expr):
    """
    Class representing a constant logical value of False in a logical formula.
    """

    def __repr__(self):
        """
        Returns a string representation of the constant False.

        Returns:
            str: The string 'ConstFalse()'.
        """
        return 'ConstFalse()'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluates the constant False.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values (not used).

        Returns:
            bool: Always False.
        """
        return False


class Var(Expr):
    """
    Class representing a variable in the logical formula.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a variable with the given name.

        Args:
            name (str): The name of the variable.
        """
        self.name = name

    def __repr__(self) -> str:
        """
        Return a string representation of the variable.

        Returns:
            str: The string representation of the variable.
        """
        return f'Var({self.name})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the variable in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The value of the variable in the given environment.
        """
        return env[self.name]


class And(Expr):
    """
    Class representing a logical AND operation.
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        """
        Initialize an AND operation with the given left and right operands.

        Args:
            left (Expr): The left operand.
            right (Expr): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the AND operation.

        Returns:
            str: The string representation of the AND operation.
        """
        return f'And({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the AND operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the AND operation.
        """
        return self.left.eval(env) and self.right.eval(env)


class Or(Expr):
    """
    Class representing a logical OR operation.
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        """
        Initialize an OR operation with the given left and right operands.

        Args:
            left (Expr): The left operand.
            right (Expr): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the OR operation.

        Returns:
            str: The string representation of the OR operation.
        """
        return f'Or({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the OR operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the OR operation.
        """
        return self.left.eval(env) or self.right.eval(env)


class Implies(Expr):
    """
    Class representing a logical implication operation.
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        """
        Initialize an implication operation with the given left and right operands.

        Args:
            left (Expr): The left operand.
            right (Expr): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the implication operation.

        Returns:
            str: The string representation of the implication operation.
        """
        return f'Implies({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the implication operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the implication operation.
        """
        return not self.left.eval(env) or self.right.eval(env)


class Equiv(Expr):
    """
    Class representing a logical equivalence operation.
    """

    def __init__(self, left: Expr, right: Expr) -> None:
        """
        Initialize an equivalence operation with the given left and right operands.

        Args:
            left (Expr): The left operand.
            right (Expr): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the equivalence operation.

        Returns:
            str: The string representation of the equivalence operation.
        """
        return f'Equiv({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the equivalence operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the equivalence operation.
        """
        return self.left.eval(env) == self.right.eval(env)


class Not(Expr):
    """
    Class representing a logical NOT operation.
    """

    def __init__(self, operand: Expr) -> None:
        """
        Initialize a NOT operation with the given operand.

        Args:
            operand (Expr): The operand.
        """
        self.operand = operand

    def __repr__(self) -> str:
        """
        Return a string representation of the NOT operation.

        Returns:
            str: The string representation of the NOT operation.
        """
        return f'Not({self.operand})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the NOT operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the NOT operation.
        """
        return not self.operand.eval(env)
