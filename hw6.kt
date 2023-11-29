import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import java.io.File
import java.net.URL

data class Location(val name: String, val lat: Double, val lon: Double) {
    companion object {
        fun from(dto: LocationDto): Location = Location(
            dto.locationInfo.city,
            dto.locationInfo.coordinates.latitude.toDouble(),
            dto.locationInfo.coordinates.longitude.toDouble())
    }
}

data class LocationResponse(val results: List<LocationDto>)

data class LocationDto(
    @JsonProperty("location")
    val locationInfo: LocationInfo
)

data class LocationInfo(
    val street: StreetInfo,
    val city: String,
    val state: String,
    val country: String,
    val postcode: Any,
    val coordinates: Coordinates,
    val timezone: Timezone
)

data class StreetInfo(val number: Int, val name: String)
data class Coordinates(val latitude: String, val longitude: String)
data class Timezone(val offset: String, val description: String)
class TravelingSalesmanProblem(private val cities: List<Location>) {
    private val distanceMatrix: Array<DoubleArray> = calculateDistanceMatrix()

    private fun calculateDistanceMatrix(): Array<DoubleArray> {
        val matrix = Array(cities.size) { DoubleArray(cities.size) }
        for (i in cities.indices) {
            for (j in cities.indices) {
                if (i != j) {
                    val distance = calculateDistance(cities[i], cities[j])
                    matrix[i][j] = distance
                }
            }
        }
        return matrix
    }

    private fun calculateDistance(city1: Location, city2: Location): Double {
        val deltaX = city1.lat - city2.lat
        val deltaY = city1.lon - city2.lon
        return Math.sqrt((deltaX * deltaX + deltaY * deltaY).toDouble())
    }

    fun solve(): List<Location> {
        val unvisitedCities = cities.toMutableList()
        val tour = mutableListOf<Location>()
        // Start from the first city
        var currentCity = unvisitedCities.removeAt(0)
        tour.add(currentCity)

        while (unvisitedCities.isNotEmpty()) {
            // Find the nearest neighbor
            val nearestNeighbor = unvisitedCities.minByOrNull { distanceMatrix[cities.indexOf(currentCity)][cities.indexOf(it)] }!!
            // Move to the nearest neighbor
            unvisitedCities.remove(nearestNeighbor)
            currentCity = nearestNeighbor
            tour.add(currentCity)
        }

        // Return to the starting city to complete the tour
        tour.add(tour[0])

        return tour
    }
//    fun displayMap() {
//        val mapUrl = buildMapUrl()
//        println("Map URL: $mapUrl")
//    }
    private fun buildMapUrl(): String {
        return "leaflet-map.html"  // Save this HTML content to a file named "leaflet-map.html"
    }
    fun displayMap() {
        val mapHtml = buildLeafletMapHtml()
        val mapFile = File("leaflet-map.html")
        mapFile.writeText(mapHtml)
        println("Map URL: ${mapFile.toURI()}")
    }

    private fun buildLeafletMapHtml(): String {
        val markerList = cities.joinToString(",") { "[${it.lat}, ${it.lon}]" }

        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <style>
                #map { height: 400px; }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <script>
                var map = L.map('map').setView([$markerList], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);

                var markers = [$markerList].forEach(function (location) {
                    L.marker([location[0], location[1]]).addTo(map);
                });
            </script>
        </body>
        </html>
    """.trimIndent()
    }

    private fun getBoundingBox(): String {
        val latitudes = cities.map { it.lat }
        val longitudes = cities.map { it.lon }
        val minLat = latitudes.minOrNull() ?: 0.0
        val maxLat = latitudes.maxOrNull() ?: 0.0
        val minLon = longitudes.minOrNull() ?: 0.0
        val maxLon = longitudes.maxOrNull() ?: 0.0

        // Adjusting the bounding box to provide some padding
        val padding = 0.1
        val adjustedMinLat = minLat - padding
        val adjustedMaxLat = maxLat + padding
        val adjustedMinLon = minLon - padding
        val adjustedMaxLon = maxLon + padding

        return "$adjustedMinLon,$adjustedMinLat,$adjustedMaxLon,$adjustedMaxLat"
    }
}

fun fetchRandomLocations(): List<Location> {
    val url = "https://api.randomuser.me/?results=5&inc=location&noinfo"
    val response = URL(url).readText()
    val objectMapper = jacksonObjectMapper()
    val results = objectMapper.readValue<LocationResponse>(response)
    return results.results.map { Location.from(it) }
}

fun main() {

    // Fetch random locations
    val randomLocations = fetchRandomLocations()

    // Solve the TSP for the random locations
    val tsp = TravelingSalesmanProblem(randomLocations)
    val solution = tsp.solve()

    // Display the map with markers for the chosen cities
    tsp.displayMap()
}
