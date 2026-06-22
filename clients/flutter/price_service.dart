import 'dart:convert';
import 'package:http/http.dart' as http;
const String kBaseUrl = 'https://your-server.example.com';
class Deal {
  final String store, originalTitle, detectedWeight;
  final double listedPrice, normalizedBasePrice;
  Deal.fromJson(Map<String, dynamic> j)
      : store = j['store'], originalTitle = j['original_title'],
        detectedWeight = j['detected_weight'],
        listedPrice = (j['listed_price'] as num).toDouble(),
        normalizedBasePrice = (j['normalized_base_price'] as num).toDouble();
}
class SearchResult {
  final String cheapestStore, normalizedUnit;
  final double lowestPriceQar, savingsQar;
  final List<Deal> deals;
  SearchResult.fromJson(Map<String, dynamic> j)
      : cheapestStore = j['cheapest_store'], normalizedUnit = j['normalized_unit'],
        lowestPriceQar = (j['lowest_price_qar'] as num).toDouble(),
        savingsQar = (j['calculated_savings_qar'] as num).toDouble(),
        deals = (j['deals'] as List).map((e) => Deal.fromJson(e)).toList();
}
Future<SearchResult> fetchCheapest(String item) async {
  final url = Uri.parse('$kBaseUrl/search?query=${Uri.encodeComponent(item)}');
  final res = await http.get(url);
  if (res.statusCode == 200) return SearchResult.fromJson(jsonDecode(res.body));
  throw Exception('Search failed: ${res.statusCode}');
}