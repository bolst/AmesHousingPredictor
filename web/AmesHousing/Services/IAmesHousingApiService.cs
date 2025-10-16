using AmesHousing.Models;

namespace AmesHousing.Services;

public interface IAmesHousingApiService
{
    Task<IEnumerable<HouseFeatures>> GetPricedHousesAsync(int page, int amount);
    Task<double> GetSalePriceAsync(HouseFeatures features);
}