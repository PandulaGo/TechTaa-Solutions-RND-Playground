using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.NetworkInformation;
using System.Threading.Tasks;

namespace RND_Playground_Apps.Projects
{
    public class BaseMainGrounds
    {
        public static void Main()
        {
            Console.WriteLine("==============================================================");
            Console.WriteLine("Base Main Grounds RND :)");
            problem1();
            problem2();
            problem3();
            Console.WriteLine("==============================================================");
        }


        public static void problem1()
        {
            List<int> numbers = new List<int> { 3, 1, 3, 2, 1 };
            List<int> uniqueNumbers = numbers.Distinct().ToList();

            foreach (var num in uniqueNumbers)
            {
                Console.WriteLine(num);
            }

            HashSet<int> uniqueSet = new();

            foreach(var num in numbers)
            {
                if(!uniqueSet.Contains(num))
                uniqueSet.Add(num);
            }

            foreach (var num in uniqueSet)
            {
                Console.WriteLine(num);
            }
        }

        public static void problem2()
        {
            string sentence = "the cat and the hat";
            string[] words = sentence.Split(' ');
            var detailList = new Dictionary<string, int>();

            foreach (var word in words)
            {
                if (detailList.ContainsKey(word))
                {
                    detailList[word]++;
                }
                else
                {
                    detailList[word] = 1;
                }
            }

            foreach (var kvp in detailList)
            {
                Console.WriteLine($"{kvp.Key}: {kvp.Value}");
            }

        }

        public static void problem3()
        {
            
        }
    }
}