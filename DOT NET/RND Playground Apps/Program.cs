var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello Pandula Goonetilleke, Welcome to the RND Playground Apps!");

RND_Playground_Apps.Projects.ValueTypeAndReferenceType.Main();
RND_Playground_Apps.Projects.Generics.Main();
RND_Playground_Apps.Projects.Reflection.Main();

app.Run();



