namespace AmesHousing.Api;

public class AmesHousingApiService : IAmesHousingApiService
{
    public async Task<GetPricedHousesResponse> GetPricedHousesAsync(int page, int amount)
    {
        throw new NotImplementedException();
    }
    
    public async Task<double> GetSalePriceAsync(AmesHouse features)
    {
        throw new NotImplementedException();
    }
}