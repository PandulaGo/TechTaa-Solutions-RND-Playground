using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RND_Playground_Apps.Projects
{
    public class ValueTypeAndReferenceType
    {
        public static void Main()
        {
            Console.WriteLine("==============================================================");
            Console.WriteLine("Value Type and Reference Type RND :)");
            ValueTypeOnly();
            ReferenceTypeOnly();
            Console.WriteLine("==============================================================");
        }

        public static void ValueTypeOnly()
        {
            int a = 10;
            int b = a; // b is a copy of a
            b = 20; // changing b does not affect a
            Console.WriteLine($"Value Type Example: a = {a}, b = {b}"); // Output: a = 10, b = 20
        }

        public static void ReferenceTypeOnly()
        {
            int[] arr1 = { 1, 2, 3 };
            int[] arr2 = arr1; // arr2 references the same array as arr1
            arr2[0] = 10; // changing arr2 affects arr1
            Console.WriteLine($"Reference Type Example: arr1[0] = {arr1[0]}, arr2[0] = {arr2[0]}"); // Output: arr1[0] = 10, arr2[0] = 10
        }
    }
}