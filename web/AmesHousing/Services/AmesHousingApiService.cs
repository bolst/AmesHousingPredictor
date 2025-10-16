using AmesHousing.Models;

namespace AmesHousing.Services;

public class AmesHousingApiService : IAmesHousingApiService
{
    public async Task<IEnumerable<HouseFeatures>> GetPricedHousesAsync(int page, int amount)
    {
        throw new NotImplementedException();
    }
    
    public async Task<double> GetSalePriceAsync(HouseFeatures features)
    {
        throw new NotImplementedException();
    }
}