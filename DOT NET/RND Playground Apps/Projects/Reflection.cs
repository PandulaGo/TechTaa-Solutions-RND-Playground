using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RND_Playground_Apps.Projects
{
    public class Reflection
    {
        public static void Main()
        {
            Console.WriteLine("==============================================================");
            Console.WriteLine("Reflection RND :)");
            ReflectionExample();
            Console.WriteLine("==============================================================");
        }

        public static void ReflectionExample()
        {


            Type type = typeof(string);
            Console.WriteLine($"Type Name: {type.Name}");
            Console.WriteLine($"Namespace: {type.Namespace}");
            Console.WriteLine($"Is Class: {type.IsClass}");
            Console.WriteLine($"Is Value Type: {type.IsValueType}");
            Console.WriteLine($"Base Type: {type.BaseType}");
        }
    }
}