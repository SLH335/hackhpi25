import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'routing.g.dart';

@riverpod
class Routing extends _$Routing {
  @override
  Future<String> build() async {
    //final Map<String, String> queryParameters = {
    //  'start': '$startAddress',
    //  'end': '$endAddress',
    //};
    //final response = await http.get(Uri.http('192.168.178.168:5000', '/way', queryParameters));
    //print("RESPONSE: __________________\n" + response.body+"\n----------------------");
    //return response.body;
    return jsonEncode({
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "LineString",
            "coordinates": [
              [-0.420679, 50.772537],
              [-0.425037, 50.778345],
            ],
          },
        },
      ],
    });
    //return data;
  }

  Future<void> getRoute(String startAddress, String endAddress) async {
    //state = AsyncData(jsonEncode({
    //  "type": "FeatureCollection",
    //  "features": [
    //    {
    //      "type": "Feature",
    //      "geometry": {
    //        "type": "LineString",
    //        "coordinates": [
    //          [-0.420679, 50.772537],
    //          [-0.425037, 50.778345],
    //        ],
    //      },
    //    },
    //  ],
    //}));
    //return;
    final Map<String, String> queryParameters = {
      'start': '$startAddress',
      'end': '$endAddress',
    };
    final response = await http.get(
      Uri.http('192.168.178.206:5000', '/way/full', queryParameters),
    );
    state = AsyncData(response.body);
  }
}
