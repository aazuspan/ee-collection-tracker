## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-11-17 14:42:26 | 2026-11-21 23:34:19 | 4 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-11-17 14:42:26 | 2026-11-21 23:34:19 | 4 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-11-10 09:28:49 | 2026-11-21 23:34:19 | 11 days      |
| **LANDSAT/LC09/C02/T1**                   | 2026-11-21 06:36:19 | 2026-11-21 23:34:19 | 17 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-11-21 06:36:19 | 2026-11-21 23:34:19 | 17 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-11-19 23:27:53 | 2026-11-21 23:34:19 | 2 days       |
| **COPERNICUS/S2**                         | 2026-11-21 21:19:17 | 2026-11-21 23:37:31 | 2 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-11-21 21:19:17 | 2026-11-21 23:37:31 | 2 hours      |
| **COPERNICUS/S2_SR**                      | 2026-11-21 20:01:51 | 2026-11-21 23:37:31 | 4 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-11-21 20:01:51 | 2026-11-21 23:37:31 | 4 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-11-19 23:28:39 | 2026-11-21 23:40:32 | 2 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-11-19 23:28:39 | 2026-11-21 23:40:32 | 2 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-11-19 23:25:06 | 2026-11-21 23:40:32 | 2 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-11-19 23:25:06 | 2026-11-21 23:40:32 | 2 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.