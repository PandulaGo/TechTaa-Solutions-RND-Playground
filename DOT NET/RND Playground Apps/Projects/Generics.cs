using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RND_Playground_Apps.Projects
{
    public class Generics
    {
        public static void Main()
        {
            Console.WriteLine("==============================================================");
            Console.WriteLine("Generics RND :)");
            GenericMethodExample<int>(42);
            GenericMethodExample<string>("Hello, Generics!");
            
            GenericClassExample<double> genericClass = new GenericClassExample<double>(3.14);
            genericClass.DisplayValue();

            IGenericInterface<int> genericInterface = new GenericInterfaceImplementation<int>();
            genericInterface.DisplayType();
            Console.WriteLine("==============================================================");
        }

        /// <summary>
        /// This is a generic method example that demonstrates how to use generics in C#.
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="input"></param>
        public static void GenericMethodExample<T>(T input)
        {
            Console.WriteLine($"Generic Method Example: Input type is {typeof(T)}, value is {input}");
        }
    }

/// <summary>
/// This is a generic class example that demonstrates how to use generics in C#.
/// </summary>
/// <typeparam name="T"></typeparam>
    public class GenericClassExample<T>
    {
        private T _value;

        public GenericClassExample(T value)
        {
            _value = value;
        }

        public void DisplayValue()
        {
            Console.WriteLine($"Generic Class Example: Value type is {typeof(T)}, value is {_value}");
        }
    }

/// <summary>
/// This is a generic interface example that demonstrates how to use generics in C#.
/// </summary>
/// <typeparam name="T"></typeparam>
    public interface IGenericInterface<T>
    {
        void DisplayType();
    }

/// <summary>
/// This is a generic interface implementation example that demonstrates how to implement a generic interface in C#.
/// </summary>
/// <typeparam name="T"></typeparam>
    public class GenericInterfaceImplementation<T> : IGenericInterface<T>
    {
        public void DisplayType()
        {
            Console.WriteLine($"Generic Interface Example: Type is {typeof(T)}");
        }
    }
}