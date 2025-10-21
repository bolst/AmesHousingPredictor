using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using AmesHousing;
using AmesHousing.Api;
using Blazored.LocalStorage;
using MudBlazor;
using MudBlazor.Services;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });

// add MudBlazor
{
    builder.Services.AddMudServices();
    MudGlobal.InputDefaults.Variant = Variant.Outlined;
    MudGlobal.InputDefaults.Margin = Margin.Dense;
    MudGlobal.Rounded = true;
    MudGlobal.GridDefaults.Spacing = 3;
}

builder.Services.AddBlazoredLocalStorage();

builder.Services.AddScoped<IAmesHousingApiService, AmesHousingApiService>();

await builder.Build().RunAsync();