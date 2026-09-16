using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Z.Expressions;

namespace RND_Playground_Apps.Projects
{
    public class EVALExpression
    {
        public static void Main()
        {
            Console.WriteLine("==============================================================");
            Console.WriteLine("EVAL Expression RND :)");
            EvaluateExpression1();
            EvaluateExpression2();
            EvaluateExpression3();
            EvaluateExpression4();
            EvaluateExpression5();
            EvaluateExpression6();
            Console.WriteLine("==============================================================");
        }

        //what is the EVAL meaning?
        // EVAL stands for "Evaluate" and is used to dynamically evaluate expressions at runtime.
    
        public static void EvaluateExpression1()
        {
            string expression = "3 + 5 * 2 - 4 / 2"; // Example expression
            var result = new System.Data.DataTable().Compute(expression, null);
            Console.WriteLine($"The result of the expression '{expression}' is: {result}");
        }

        public static void EvaluateExpression2()
        {
            // Sample Expression Evaluation.
            string expression = "2+3*4";
            var result1 = Eval.Execute<int>(expression);
            ValidateExpression(expression);
            Console.WriteLine($"Result of {expression}':' {result1}");
            Console.WriteLine($"===================================================================");
        }

        public static void EvaluateExpression3()
        {
            //Variable Usage
            int x = 10;
            string expression = "x * 2";
            var result = Eval.Execute<int>(expression, new {x});
            ValidateExpression(expression, new {x});
            Console.WriteLine($"Result of {expression} with x={x}: {result}");
            Console.WriteLine($"===================================================================");
        }

        public static void EvaluateExpression4()
        {
            // Complext Expression with multiple variables
            int a = 5;
            int b = 4;

            string expression3 = "a > b ? a + b : a - b";
            var result3 = Eval.Execute<int>(expression3, new { a, b });
            ValidateExpression(expression3);	
            Console.WriteLine($"Result of {expression3}':' {result3}");
            Console.WriteLine($"===================================================================");
        }

        public static void EvaluateExpression5()
        {
            // String Manipulation
            string name = "Pandula Goonetilleke";
            string expression4 = $"\"Hello, {name}!\"";
            var result4 = Eval.Execute<string>(expression4, new { name });
            ValidateExpression(expression4, name);
            Console.WriteLine($"Result of '{expression4}': {result4}");
            Console.WriteLine($"===================================================================");
        }

        public static void EvaluateExpression6()
        {
            //Compilation and repeated execution
            string compiledExpression = "y * y";
            var compiledFunc = Eval.Compile<Func<int, int>>(compiledExpression, "y");
            int result5 = compiledFunc(5);
            Console.WriteLine($"Result of '{result5}");
            Console.WriteLine($"===================================================================");

            int result6 = compiledFunc(10);
            Console.WriteLine($"Result of '{result6}");
            Console.WriteLine($"===================================================================");
        }
        

        public static bool ValidateExpression(string expression,  dynamic variables = null)
	{
		try
		{
			if (variables == null)
				Eval.Compile(expression, variables);

			else
				Eval.Execute(expression, variables);

			Console.WriteLine($"Is Valid Expression : True");
			return true;
		}
		catch (Exception ex)
		{
			Console.WriteLine($"Is Valid Expression : False");
			return false;
			throw;
		}
	}
    }
}