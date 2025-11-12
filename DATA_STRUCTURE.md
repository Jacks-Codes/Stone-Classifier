# Stone_Data Directory Structure

This document describes the complete directory structure for the stone classifier dataset.

## Overview

```
Stone_Data/
├── train/          # Training images (70-80% of data)
│   ├── granite/    # 84 granite types
│   ├── marble/     # 10 marble types
│   ├── quartz/     # 118 quartz types
│   ├── quartzite/  # 39 quartzite types
│   └── travertine/ # 11 travertine types
└── val/            # Validation images (20-30% of data)
    ├── granite/    # 84 granite types
    ├── marble/     # 10 marble types
    ├── quartz/     # 118 quartz types
    ├── quartzite/  # 39 quartzite types
    └── travertine/ # 11 travertine types
```

**Total Stone Types: 262**

## Directory Structure Details

### Granite (84 types)

Located in: `Stone_Data/train/granite/` and `Stone_Data/val/granite/`

```
granite/
├── absolute_black/
├── african_rainbow/
├── agatha_black/
├── alpine_valley/
├── amarello_ornamental/
├── andino_white/
├── arctic_sand/
├── aspen_white/
├── astoria/
├── avalon_white/
├── azul_celeste/
├── azul_platino/
├── azure_mist/
├── bianco_antico/
├── bianco_frost/
├── black_forest/
├── black_galaxy/
├── black_pearl/
├── blue_pearl/
├── caledonia/
├── caravelas_gold/
├── ceara_white/
├── coffee_brown/
├── colonial_cream/
├── colonial_ice/
├── colonial_white/
├── costa_esmeralda/
├── crema_atlantico/
├── crema_caramel/
├── cygnus/
├── delicatus_white/
├── desert_beach/
├── desert_dream/
├── eclipse/
├── everest_mist/
├── ferro_gold/
├── fortaleza/
├── giallo_ornamental/
├── gran_valle/
├── gray_mist/
├── gray_nuevo/
├── himalaya_white/
├── lennon/
├── luna_pearl/
├── makalu_bay/
├── mirage_white/
├── monte_cristo/
├── nero_mist/
├── new_river_white/
├── new_venetian_gold/
├── oyster_white/
├── patagonia/
├── pitaya_white/
├── premium_black/
├── s_f_real/
├── salinas_white/
├── santa_cecelia/
├── santa_cecelia_lc/
├── santana/
├── sapphire_blue/
├── silver_cloud/
├── silver_falls/
├── silver_waves/
├── snowfall/
├── solarius/
├── steel_grey/
├── stream_white/
├── sunset_canyon/
├── titanium/
├── typhoon_bordeaux/
├── ubatuba/
├── valle_nevado/
├── via_lactea/
├── virginia_mist/
├── white_alpha/
├── white_galaxy/
├── white_ice/
├── white_napoli/
├── white_ornamental/
├── white_sand/
├── white_sparkle/
├── white_spring/
├── white_valley/
└── white_wave/
```

### Marble (10 types)

Located in: `Stone_Data/train/marble/` and `Stone_Data/val/marble/`

```
marble/
├── absolute_white/
├── arabescus_white/
├── calacatta_marble/
├── carrara_white/
├── elegant_white/
├── fantasy_brown/
├── fantasy_river/
├── fantasy_white/
├── portinari_marble/
└── super_white/
```

### Quartz (118 types)

Located in: `Stone_Data/train/quartz/` and `Stone_Data/val/quartz/`

#### Calacatta Varieties (50+ types)
```
quartz/
├── calacatta_abezzo/
├── calacatta_adonia/
├── calacatta_aidana/
├── calacatta_alto/
├── calacatta_anava/
├── calacatta_arno/
├── calacatta_azai/
├── calacatta_azulean/
├── calacatta_bali/
├── calacatta_belaros/
├── calacatta_botanica/
├── calacatta_castana/
├── calacatta_cinela/
├── calacatta_clara/
├── calacatta_classique/
├── calacatta_delios/
├── calacatta_duolina/
├── calacatta_elysio/
├── calacatta_fioressa/
├── calacatta_goa/
├── calacatta_idillio/
├── calacatta_izaro/
├── calacatta_karmelo/
├── calacatta_lapiza/
├── calacatta_lavasa/
├── calacatta_laza/
├── calacatta_laza_grigio/
├── calacatta_laza_night/
├── calacatta_laza_oro/
├── calacatta_leon/
├── calacatta_leon_gold/
├── calacatta_luccia/
├── calacatta_lumanyx/
├── calacatta_miraggio/
├── calacatta_miraggio_cielo/
├── calacatta_miraggio_cove/
├── calacatta_miraggio_duo/
├── calacatta_miraggio_gold/
├── calacatta_miraggio_lusso/
├── calacatta_miraggio_seaglass/
├── calacatta_miraggio_sienna/
├── calacatta_monaco/
├── calacatta_ocellio/
├── calacatta_prado/
├── calacatta_premata/
├── calacatta_rusta/
├── calacatta_safyra/
├── calacatta_sierra/
├── calacatta_solessio/
├── calacatta_trevi/
├── calacatta_ultra/
├── calacatta_valentin/
├── calacatta_venice/
├── calacatta_vernello/
├── calacatta_verona/
├── calacatta_versailles/
├── calacatta_vicenza/
├── calacatta_viraldi/
├── new_calacatta_laza/
└── new_calacatta_laza_gold/
```

#### Carrara Varieties
```
quartz/
├── carrara_breve/
├── carrara_delphi/
├── carrara_lumos/
├── carrara_marmi/
├── carrara_miksa/
├── carrara_mist/
├── carrara_morro/
├── carrara_trigato/
└── new_carrara_marmi/
```

#### Other Quartz Types
```
quartz/
├── alabaster_white/
├── arctic_white/
├── aruca_white/
├── aurataj/
├── azurmatt/
├── babylon_gray/
├── bayshore_sand/
├── bianco_pepper/
├── blanca_arabescato/
├── blanca_statuarietto/
├── calico_white/
├── cashmere_carrara/
├── cashmere_taj/
├── chakra_beige/
├── concerto/
├── eroluna/
├── fairy_white/
├── fossil_gray/
├── frost_white/
├── galant_gray/
├── glacier_white/
├── gray_lagoon/
├── iced_gray/
├── iced_white/
├── ivoritaj/
├── lumataj/
├── macabo_gray/
├── manhattan_gray/
├── marfitaj/
├── marquina_midnight/
├── meridian_gray/
├── midnight_corvo/
├── midnight_majesty/
├── montclair_white/
├── mystic_gray/
├── peppercorn_white/
├── perla_white/
├── portico_cream/
├── premium_plus_white/
├── rolling_fog/
├── smoked_pearl/
├── snow_white/
├── soapstone_metropolis/
├── soapstone_mist/
├── solitaj/
├── sparkling_black/
├── sparkling_white/
├── statuary_classique/
└── stellar_white/
```

### Quartzite (39 types)

Located in: `Stone_Data/train/quartzite/` and `Stone_Data/val/quartzite/`

```
quartzite/
├── aquatic/
├── allure/
├── andes_black/
├── audacia/
├── azul_imperiale/
├── azul_macaubas/
├── azul_treasure/
├── belvedere/
├── blue_fusion/
├── blue_lava/
├── blue_roma/
├── calacatta_macaubas/
├── calacatta_montreal/
├── cirrus_gray/
├── cristallo/
├── crytos/
├── denali/
├── fantasy_macaubas/
├── fantasy_montreal/
├── florida_wave/
├── fusion/
├── galapagos/
├── glacier_wave/
├── gray_canyon/
├── kalahari/
├── madreperola/
├── mercury_gray/
├── milano/
├── onyx_bamboo/
├── patagonia_green/
├── platinum_black/
├── platinum_blue/
├── platinum_gray/
├── sea_pearl/
├── taj_mahal/
├── tempest/
├── white_macaubas/
├── white_montreal/
└── zermat/
```

### Travertine (11 types)

Located in: `Stone_Data/train/travertine/` and `Stone_Data/val/travertine/`

```
travertine/
├── bianco_navona_travertine/
├── burgundy_travertine/
├── chocolate_travertine/
├── classic_travertine/
├── crema_travertine/
├── gold_travertine/
├── noce_travertine/
├── persian_red_travertine_extra/
├── roman_travertine/
├── silver_travertine/
└── walnut_travertine/
```

## Image Organization

### File Naming Convention

Images are stored directly in each stone type folder with descriptive names:
- Format: `{stone_type}_{number}.jpg` or `{stone_type}_{number}.png`
- Example: `absolute_black_0001.jpg`, `calacatta_azulean_0042.jpg`

### Train/Validation Split

- **Training Set**: 70-80% of images per stone type
  - Location: `Stone_Data/train/{category}/{stone_type}/`
  - Used for model training

- **Validation Set**: 20-30% of images per stone type
  - Location: `Stone_Data/val/{category}/{stone_type}/`
  - Used for model evaluation during training

### Recommended Image Counts

- **Minimum**: 50-100 images per stone type
- **Recommended**: 100-200 images per stone type
- **Ideal**: 200-500+ images per stone type

### Image Requirements

- **Format**: JPG, JPEG, or PNG
- **Minimum Size**: 50KB (filters out placeholders)
- **Quality**: Clear, well-lit images
- **Variety**: Different lighting, angles, backgrounds

## Usage in Training

The `train_model.py` script automatically:
1. Discovers all stone types from folder structure
2. Creates class indices based on folder names
3. Loads images from `train/` for training
4. Uses images from `val/` for validation
5. Saves class indices to `class_indices.json`

## Statistics

- **Total Categories**: 5 (granite, marble, quartz, quartzite, travertine)
- **Total Stone Types**: 262
  - Granite: 84
  - Marble: 10
  - Quartz: 118
  - Quartzite: 39
  - Travertine: 11
- **Expected Total Images** (at 100 per type): ~26,200 images
- **Storage Estimate**: ~12-50 GB (depending on image sizes)

## Notes

- All folder names use lowercase with underscores (e.g., `absolute_black`, `calacatta_azulean`)
- Folder names must match exactly between `train/` and `val/` directories
- The model automatically detects classes from folder names
- Empty folders are allowed (script will download images to them)

