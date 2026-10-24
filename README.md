## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-19 15:05:59 | 2026-10-24 23:34:55 | 5 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-19 15:05:59 | 2026-10-24 23:34:55 | 5 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-17 10:04:58 | 2026-10-24 23:34:55 | 7 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-23 03:46:15 | 2026-10-24 23:34:55 | a day        |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-23 03:46:15 | 2026-10-24 23:34:55 | a day        |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-22 23:03:33 | 2026-10-24 23:34:55 | 2 days       |
| **COPERNICUS/S2**                         | 2026-10-24 21:00:14 | 2026-10-24 23:37:53 | 3 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-24 21:00:14 | 2026-10-24 23:37:53 | 3 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-24 20:19:58 | 2026-10-24 23:37:53 | 3 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-24 20:19:58 | 2026-10-24 23:37:53 | 3 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-22 17:54:01 | 2026-10-24 23:40:30 | 2 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-22 17:54:01 | 2026-10-24 23:40:30 | 2 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-22 21:50:55 | 2026-10-24 23:40:30 | 2 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-22 21:50:55 | 2026-10-24 23:40:30 | 2 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.