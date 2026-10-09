using Microsoft.AspNetCore.Authentication;
using Microsoft.IdentityModel.Tokens;
using Google.Apis.Auth;


var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello Pandula Goonetilleke, Welcome to the RND Playground Apps!");

RND_Playground_Apps.Projects.ValueTypeAndReferenceType.Main();
RND_Playground_Apps.Projects.Generics.Main();
RND_Playground_Apps.Projects.Reflection.Main();
RND_Playground_Apps.Projects.EVALExpression.Main();

var builder = WebApplication.CreateBuilder(args);

var googleClientId = builder.configuration["Authentication:Google:ClientId"] ?? throw new InvalidOperationException("Google Client ID is missing!");

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        // Ask Google's OpenID Connect metadata for its signing keys automatically.
        // .NET will fetch https://accounts.google.com/.well-known/openid-configuration
        // and handle key rotation for you.
        options.Authority = "https://accounts.google.com";
        options.Audience = googleClientId;

        // Extra safety: Google should be the ONLY issuer we trust.
        options.TokenValidationParameters.IssuerValidator = (issuer, token, parameters) =>
            issuer is "accounts.google.com" or "https://accounts.google.com"
                ? issuer
                : throw new SecurityTokenInvalidIssuerException("Unknown issuer: " + issuer);
    });

builder.Services.AddAuthorization();
var app = builder.Build();

app.UseAuthentication():
app.UseAuthorization();

app.MapGet("", () => "Public endpoint - no login needed.");

app.MapGet("/me", (ClaimsPrincipal user) =>
    Results.Ok(new
    {
        Name = user.Identity?.Name,
        Email = user.FindFirstValue("email"),
        GoogleUserId = user.FindFirstValue(System.Security.Claims.ClaimTypes.NameIdentifier),
    })).RequireAuthorization();

app.MapPost("/google-login", async (LoginRequest request, string? clientId) =>
{
    // request.Credential  <- the ID token the SPA sent (Google GSI also sends a CSRF cookie)
    if (clientId is null) return Results.BadRequest();
    try
    {
        var user = await VerifyGoogleTokenAsync(request.Credential, clientId);
        // now create your own app session / JWT for THIS user
        return Results.Ok(user);
    }
    catch (InvalidJwtException)
    {
        return Results.Unauthorized();
    }
});

app.Run();

using System.Security.Claims;




public record GoogleUser(string sub, string Email, string Name, string? Picture);

public static async Task<GoogleUser> ValidateGoogleTokenAsync(string idToken, string clientId)
{
    var payload = await GoogleJsonWebSignature.ValidateAsync(idToken, new GoogleJsonWebSignature.ValidationSettings
    {
        Audience = new[] { clientId }
    });
    return new GoogleUser(payload.Subject, payload.Email, payload.Name, payload.Picture);
}


