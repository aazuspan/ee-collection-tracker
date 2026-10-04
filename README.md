## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-09-27 07:29:01 | 2026-10-04 23:38:50 | 7 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-09-27 07:29:01 | 2026-10-04 23:38:50 | 7 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-09-27 05:39:46 | 2026-10-04 23:38:50 | 7 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-04 03:24:31 | 2026-10-04 23:38:50 | 20 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-04 03:24:31 | 2026-10-04 23:38:50 | 20 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-02 23:27:52 | 2026-10-04 23:38:50 | 2 days       |
| **COPERNICUS/S2**                         | 2026-10-04 21:53:56 | 2026-10-04 23:42:27 | 2 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-04 21:53:56 | 2026-10-04 23:42:27 | 2 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-04 19:23:18 | 2026-10-04 23:42:27 | 4 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-04 19:23:18 | 2026-10-04 23:42:27 | 4 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-02 23:46:19 | 2026-10-04 23:45:30 | a day        |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-02 23:46:19 | 2026-10-04 23:45:30 | a day        |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-02 23:54:31 | 2026-10-04 23:45:30 | a day        |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-02 23:54:31 | 2026-10-04 23:45:30 | a day        |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.