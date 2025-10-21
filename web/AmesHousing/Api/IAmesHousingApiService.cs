namespace AmesHousing.Api;

public interface IAmesHousingApiService
{
    Task<IEnumerable<AmesHouse>> GetPricedHousesAsync(int page, int amount);
    Task<double> GetSalePriceAsync(AmesHouse features);
}