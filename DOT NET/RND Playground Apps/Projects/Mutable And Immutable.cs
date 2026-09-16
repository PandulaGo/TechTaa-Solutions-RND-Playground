using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;

namespace RND_Playground_Apps.Projects;
public class MutableAndImmutable
{
    public static void Main()
    {
        Console.WriteLine("==============================================================");
        Console.WriteLine("Mutable and Immutable RND :)");
        MutableExample();
        ImmutableExample();
        Console.WriteLine("==============================================================");
    }

    public static void MutableExample()
    {
        List<int> mutableList = new List<int> { 1, 2, 3 };
        mutableList.Add(4); // Modifying the list
        Console.WriteLine($"Mutable Example: List contents are {string.Join(", ", mutableList)}"); // Output: 1, 2, 3, 4
    }

    public static void ImmutableExample()
    {
    ImmutableList<int> immutableList = ImmutableList.Create(1, 2, 3);

    // Calling .Add() returns a NEW list; it does not change 'immutableList'
    ImmutableList<int> newList = immutableList.Add(4); 

    Console.WriteLine($"Original List: {string.Join(", ", immutableList)}"); // Output: 1, 2, 3
    Console.WriteLine($"New List: {string.Join(", ", newList)}");           // Output: 1, 2, 3, 4
    }
}
