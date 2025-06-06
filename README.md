# E57 Metadata Extractor for Archivematica

This repository provides a script to extract metadata from ASTM E57 files in [Archivematica](https://www.archivematica.org/) using the [libE57 tools](http://www.libe57.org/download.html) tool.

## Installation

To install this script, follow these steps:

### 1. Download the official E57 validator tool

- Download the latest release for Windows x86 (64bit) of the [E57 validator](http://www.libe57.org/download.html) and put the `./bin/e57xmldump.exe` in the `/usr/share/` folder.

### 2. Install Wine

- Install [Wine](https://www.winehq.org/) e. g. by entering the commands in the terminal: `sudo apt install wine64`.

### 3. Create a new format policy tool

- In the Archivematica frontend, navigate to **Preservation planning** > **Format policy registry** > **Tools** > **Create new tool** or go directly to [this link](http://10.10.10.20/fpr/fptool/create/).
- Enter the following parameters:
  - **Description**: Enter `e57xmldump`.
  - **Version**: Enter the version you downloaded, e. g. `1.1.312`.
- Click **Save**.

### 4. Create a new characterization command

- In the Archivematica frontend, navigate to **Preservation planning** > **Characterization** > **Commands** > **Create new command** or go directly to [this link](http://10.10.10.20/fpr/fpcommand/create/).
- Fill in the following fields:
  - **The related tool**: Select **e57xmldump**.
  - **Description**: Enter `Characterize using e57xmldump`.
  - **Command**: Paste the entire content of the [**e57-metadata-extractor.py**](./src/e57-metadata-extractor.py) file.
  - **Script type**: Select **Python script**.
  - **The related output format**: Select **Text (Markup): XML: XML (fmt/101)**.
  - **Command usage**: Select **Characterization**.
  - Leave all other input fields and combo boxes untouched.
- Click **Save**.

### 5. Create a new characterization rule E57

- In the Archivematica frontend, navigate to **Preservation planning** > **Characterization** > **Rules** > **Create new rule** or go directly to [this link](http://10.10.10.20/fpr/fprule/create/).
- Fill in the following fields:
  - **Purpose**: Select **Characterization**.
  - **The related format**: Select **Image (Vector): ASTM E57 3D File Format: E57 3D File Format (fmt/643)**.
  - **Command**: Select **Characterize using e57xmldump**.
- Click **Save**.

## Test

To test this metadata exctractor, you can use the sample E57 files located [here](https://github.com/JoergHeseler/point-cloud-samples-for-preservation-testing/tree/main/e57).

### In Archivematica:

You can view the error codes and detailed characterization results in the Archivmatica frontend after starting a transfer by expanding the `▸ Microservice: Characterize and extract metadata` section and clicking on the gear icon of `Microservice: Characterize and extract metadata`.

Valid files should pass characterization with this script and return error code **0**. However, files containing errors should fail characterization and either return error code **1** or **255**.

### In the command line:

You can use the validator at the command line prompt by typing `python e57-metadata-extractor.py --file-full-name=<E57 file to characterize>`. You may also want to add `--validator-path=<path to the e57xmldump>`.

### Example

If you use this script to characterize the E57 model [`cockatoo-e57-1.0-color_transferred-valid.e57`](https://github.com/JoergHeseler/point-cloud-samples-for-preservation-testing/blob/main/e57/cockatoo-e57-1.0-color_transferred-valid), the error code **0** should be returned and the following XML content will be included in the AIP's METS document in the <objectCharacteristicsExtension> element of the file:

```xml
<?xml version="1.0" ?>
<E57MetadataExtractor xmlns="http://nfdi4culture.de/e57-metadata-extractor1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nfdi4culture.de/e57-metadata-extractor1 https://raw.githubusercontent.com/JoergHeseler/e57-metadata-extractor-for-archivematica/refs/heads/main/src/e57-metadata-extractor.xsd">
    <formatName>E57 (ASTM E57 3D Imaging Data File)</formatName>
    <formatVersion>1.0</formatVersion>
    <size>14074880</size>
    <SHA256Checksum>45c2b120c7e4e9ec41aaa592b4e7963b62ac396e51b9083cfce3e36413145e58</SHA256Checksum>
    <creationDate>2025-04-30T08:18:11.397547</creationDate>
    <modificationDate>2025-01-14T14:52:31.466197</modificationDate>
    <library>E57Format-2.2.0-AMD64_64-windows</library>
    <scanCount>1</scanCount>
    <hasColoredScans>true</hasColoredScans>
    <totalPointCount>518889</totalPointCount>
    <imageCount>0</imageCount>
    <rawE57XmlDumpOutput>
<![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<e57Root type="Structure"
         xmlns="http://www.astm.org/COMMIT/E57/2010-e57-v1.0"
         xmlns:nor="http://www.libe57.org/E57_NOR_surface_normals.txt">
  <formatName type="String"><![CDATA[ASTM E57 3D Imaging Data File]]]]><![CDATA[></formatName>
  <guid type="String"><![CDATA[{233FB646-7CBC-4B4B-750F-2B54793346A5}]]]]><![CDATA[></guid>
  <versionMajor type="Integer">1</versionMajor>
  <versionMinor type="Integer"/>
  <e57LibraryVersion type="String"><![CDATA[E57Format-2.2.0-AMD64_64-windows]]]]><![CDATA[></e57LibraryVersion>
  <data3D type="Vector" allowHeterogeneousChildren="1">
    <vectorChild type="Structure">
      <guid type="String"><![CDATA[{aa9ade13-58b5-403b-a810-a3883ae3effb}]]]]><![CDATA[></guid>
      <colorLimits type="Structure">
        <colorRedMaximum type="Integer">255</colorRedMaximum>
        <colorRedMinimum type="Integer"/>
        <colorGreenMaximum type="Integer">255</colorGreenMaximum>
        <colorGreenMinimum type="Integer"/>
        <colorBlueMaximum type="Integer">255</colorBlueMaximum>
        <colorBlueMinimum type="Integer"/>
      </colorLimits>
      <pose type="Structure">
        <rotation type="Structure">
          <w type="Float">1.00000000000000000e+00</w>
          <x type="Float"/>
          <y type="Float"/>
          <z type="Float"/>
        </rotation>
        <translation type="Structure">
          <x type="Float"/>
          <y type="Float"/>
          <z type="Float"/>
        </translation>
      </pose>
      <points type="CompressedVector" fileOffset="48" recordCount="518889">
        <prototype type="Structure">
          <cartesianX type="Float" precision="single"/>
          <cartesianY type="Float" precision="single"/>
          <cartesianZ type="Float" precision="single"/>
          <colorRed type="Integer" minimum="0" maximum="255"/>
          <colorGreen type="Integer" minimum="0" maximum="255"/>
          <colorBlue type="Integer" minimum="0" maximum="255"/>
          <nor:normalX type="Float" precision="single" minimum="-1.0000000e+00" maximum="1.0000000e+00"/>
          <nor:normalY type="Float" precision="single" minimum="-1.0000000e+00" maximum="1.0000000e+00"/>
          <nor:normalZ type="Float" precision="single" minimum="-1.0000000e+00" maximum="1.0000000e+00"/>
        </prototype>
        <codecs type="Vector" allowHeterogeneousChildren="1">
        </codecs>
      </points>
    </vectorChild>
  </data3D>
  <images2D type="Vector" allowHeterogeneousChildren="1">
  </images2D>
</e57Root>]]>    </rawE57XmlDumpOutput>
</E57MetadataExtractor>
```

## Dependencies

[Archivematica 1.13.2](https://github.com/artefactual/archivematica/releases/tag/v1.13.2) and [libE57 tools 1.1.312](http://www.libe57.org/download.html) were used to analyze, design, develop and test this script.

## Background

As part of the [NFDI4Culture](https://nfdi4culture.de/) initiative, efforts are underway to enhance the capabilities of open-source digital preservation software like Archivematica to identify, validate and characterize 3D file formats. This repository provides a script to improve metadata extraction of E57 files in Archivematica, enhancing its 3D content preservation capabilities.

## Related Projects

- [NFDI4Culture 3D Reference Implementations](https://github.com/JoergHeseler/nfdi4culture-3d-reference-implementations)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

Special thanks to the colleagues from the SLUB Dresden, specifically from the Infrastructure and Long-Term Availability division, for their support and valuable feedback during the development.

## Imprint

[NFDI4Culture](https://nfdi4culture.de/) – Consortium for Research Data on Material and Immaterial Cultural Heritage.  
Funded by the German Research Foundation (DFG), Project No. [441958017](https://gepris.dfg.de/gepris/projekt/441958017).

**Author**: [Jörg Heseler](https://orcid.org/0000-0002-1497-627X)  
**License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
