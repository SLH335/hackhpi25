import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:permission_handler/permission_handler.dart';

class MapScreen extends ConsumerStatefulWidget {
  const MapScreen({super.key});

  @override
  ConsumerState<ConsumerStatefulWidget> createState() => _MapScreenState();
}

class _MapScreenState extends ConsumerState<MapScreen> {
  late MapboxMap mapboxMap;
  PointAnnotationManager? pointAnnotationManager;


  _onMapCreated(MapboxMap mapboxMap) async {
    this.mapboxMap = mapboxMap;
    await Permission.location.request();

    // Enable location component with 3D duck puck
    await mapboxMap.location.updateSettings(
      LocationComponentSettings(
        enabled: true,
        locationPuck: LocationPuck(
          locationPuck3D: LocationPuck3D(
            modelUri: "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF-Embedded/Duck.gltf",
            modelScale: [40, 40, 40], // Adjust scale as needed
            modelTranslation: [0.0, 0.0, 0.0],
          ),
        ),
      ),
    );
    pointAnnotationManager =
    await mapboxMap.annotations.createPointAnnotationManager();

    // Load the image from assets

    try {
      final ByteData bytes = await rootBundle.load('assets/images/icon.png');
      final Uint8List imageData = bytes.buffer.asUint8List();

      // Create a PointAnnotationOptions
      PointAnnotationOptions pointAnnotationOptions = PointAnnotationOptions(
        //geometry: Point(coordinates: Position(-74.00913, 40.75183)), // Example coordinates
        geometry: Point(
          coordinates: Position(13.1292584, 52.3920919),
        ), // Example coordinates
        //iconColor: 50,
        image: imageData,
        iconSize: 3.0,
      );

      // Add the annotation to the map
      pointAnnotationManager?.create(pointAnnotationOptions);
    } catch (e) {
    debugPrint("❌ Failed to load icon: $e");
    }

  }

  _addRouteLine() async {
    await mapboxMap.style.addLayer(
      LineLayer(
        id: "line-layer",
        sourceId: "line",
        lineBorderColor: Colors.black.value,
        // Defines a line-width, line-border-width and line-color at different zoom extents
        // by interpolating exponentially between stops.
        // Doc: https://docs.mapbox.com/style-spec/reference/expressions/
        lineWidthExpression: [
          'interpolate',
          ['exponential', 1.5],
          ['zoom'],
          4.0,
          6.0,
          10.0,
          7.0,
          13.0,
          9.0,
          16.0,
          3.0,
          19.0,
          7.0,
          22.0,
          21.0,
        ],
        lineBorderWidthExpression: [
          'interpolate',
          ['exponential', 1.5],
          ['zoom'],
          9.0,
          1.0,
          16.0,
          3.0,
        ],
        lineColorExpression: [
          'interpolate',
          ['linear'],
          ['zoom'],
          8.0,
          'rgb(51, 102, 255)',
          11.0,
          [
            'coalesce',
            ['get', 'route-color'],
            'rgb(51, 102, 255)',
          ],
        ],
      ),
    );
  }

  _onStyleLoadedCallback(StyleLoadedEventData data) async {
    final data = await rootBundle.loadString('assets/route.geojson');
    await mapboxMap.style.addSource(GeoJsonSource(id: "line", data: data));
    await _addRouteLine();
  }

  _showBottomSheet() {
    return showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent, // ← Makes outer area see-through
      builder: (BuildContext context) {
        return Padding(
          padding: const EdgeInsets.only(
            left: 16.0,
            right: 16.0,
            top: 24.0,
            bottom: 16.0,
          ),
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(24),
            ),
            padding: EdgeInsets.only(
              bottom: MediaQuery
                  .of(context)
                  .viewInsets
                  .bottom,
              left: 16,
              right: 16,
              top: 24,
            ),
            child: SizedBox(
              height: 250,
              child: ListView(
                children: [
                  TextField(
                    decoration: InputDecoration(
                      hintText: "Start",
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextField(
                    decoration: InputDecoration(
                      hintText: "End",
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      ElevatedButton.icon(
                        icon: const Icon(Icons.navigation),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.grey.shade300,
                          foregroundColor: Colors.black,
                        ),
                        onPressed: () {},
                        label: const Text("Navigation"),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }



  @override
  Widget build(BuildContext context) {

    // WidgetsFlutterBinding.ensureInitialized();


    // Pass your access token to MapboxOptions so you can load a map
    String ACCESS_TOKEN = dotenv.env['MAPBOX_TOKEN'] ?? "";
    if (ACCESS_TOKEN.isEmpty) {
      debugPrint("❌ MAPBOX_TOKEN is missing! Did you load .env?");
    }


    MapboxOptions.setAccessToken(ACCESS_TOKEN);

    // Define options for your camera
    CameraOptions camera = CameraOptions(
      center: Point(coordinates: Position(13.1324002, 52.3938577)),
      zoom: 20,
      bearing: 0,
      pitch: 30,
    );

    // Run your application, passing your CameraOptions to the MapWidget
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.grey.shade50,
        child: Icon(Icons.navigation_outlined, size: 35, color: Colors.black),
        onPressed: () {
          _showBottomSheet();
        },
      ),
      //bottomSheet: _showBottomSheet(),
      body: MapWidget(
        cameraOptions: camera,
        onMapCreated: _onMapCreated,
        onStyleLoadedListener: _onStyleLoadedCallback,
      ),
    );
  }
}



