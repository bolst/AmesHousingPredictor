namespace AmesHousing.Api;

public interface IAmesHousingApiService
{
    Task<GetPricedHousesResponse> GetPricedHousesAsync(int page, int amount);
    Task<double> GetSalePriceAsync(AmesHouse features);
}