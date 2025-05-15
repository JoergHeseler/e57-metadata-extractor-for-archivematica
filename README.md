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
    <formatName>ASTM E57 3D Imaging Data File</formatName>
    <formatVersion>1.0</formatVersion>
    <size>14075904</size>
    <SHA256Checksum>5f637c6f617d162adc9a49a697e2ec362280307e0f9204fe89dbf8ed4b3201dd</SHA256Checksum>
    <creationDate>2025-05-15T09:00:35.559343</creationDate>
    <modificationDate>2025-05-15T09:00:36.222565</modificationDate>
    <library>E57Format-3.1.1-AMD64_64-vc1916</library>
    <totalScanCount>1</totalScanCount>
    <hasColoredScans>true</hasColoredScans>
    <totalPointCount>518889</totalPointCount>
    <totalImageCount>0</totalImageCount>
    <rawE57XmlDumpOutput>
<![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<e57Root type="Structure"
         xmlns="http://www.astm.org/COMMIT/E57/2010-e57-v1.0"
         xmlns:nor="http://www.libe57.org/E57_NOR_surface_normals.txt">
  <formatName type="String"><![CDATA[ASTM E57 3D Imaging Data File]]]]><![CDATA[></formatName>
  <guid type="String"><![CDATA[{30a6a09e-310b-4cfd-990a-503cc334d181}]]]]><![CDATA[></guid>
  <versionMajor type="Integer">1</versionMajor>
  <versionMinor type="Integer"/>
  <e57LibraryVersion type="String"><![CDATA[E57Format-3.1.1-AMD64_64-vc1916]]]]><![CDATA[></e57LibraryVersion>
  <coordinateMetadata type="String"/>
  <creationDateTime type="Structure">
    <dateTimeValue type="Float"/>
    <isAtomicClockReferenced type="Integer"/>
  </creationDateTime>
  <data3D type="Vector" allowHeterogeneousChildren="1">
    <vectorChild type="Structure">
      <guid type="String"><![CDATA[{a4f1ec4b-75fa-4e3d-9a03-0ee34d1e1da8}]]]]><![CDATA[></guid>
      <name type="String"><![CDATA[cockatoo-ply-1.0_binary-unmodified-unknown - Cloud]]]]><![CDATA[></name>
      <description type="String"><![CDATA[Created by CloudCompare v2.13.2 (Kharkiv - Jul  6 2024)]]]]><![CDATA[></description>
      <colorLimits type="Structure">
        <colorRedMinimum type="Integer"/>
        <colorRedMaximum type="Integer">255</colorRedMaximum>
        <colorGreenMinimum type="Integer"/>
        <colorGreenMaximum type="Integer">255</colorGreenMaximum>
        <colorBlueMinimum type="Integer"/>
        <colorBlueMaximum type="Integer">255</colorBlueMaximum>
      </colorLimits>
      <cartesianBounds type="Structure">
        <xMinimum type="Float">-1.35499944686889648e+01</xMinimum>
        <xMaximum type="Float">1.06771125793457031e+01</xMaximum>
        <yMinimum type="Float">7.80896702781319618e-03</yMinimum>
        <yMaximum type="Float">2.07065315246582031e+01</yMaximum>
        <zMinimum type="Float">-5.19243621826171875</zMinimum>
        <zMaximum type="Float">5.3844757080078125</zMaximum>
      </cartesianBounds>
      <points type="CompressedVector" fileOffset="48" recordCount="518889">
        <prototype type="Structure">
          <cartesianX type="Float" precision="single" minimum="-1.3549994e+01" maximum="1.0677113e+01">-1.4364409</cartesianX>
          <cartesianY type="Float" precision="single" minimum="7.808967e-03" maximum="2.0706532e+01">1.035717e+01</cartesianY>
          <cartesianZ type="Float" precision="single" minimum="-5.1924362" maximum="5.3844757">9.6019745e-02</cartesianZ>
          <nor:normalX type="Float" precision="single" minimum="-1" maximum="1"/>
          <nor:normalY type="Float" precision="single" minimum="-1" maximum="1"/>
          <nor:normalZ type="Float" precision="single" minimum="-1" maximum="1"/>
          <colorRed type="Integer" minimum="0" maximum="255"/>
          <colorGreen type="Integer" minimum="0" maximum="255"/>
          <colorBlue type="Integer" minimum="0" maximum="255"/>
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

[Archivematica 1.13.2](https://github.com/artefactual/archivematica/releases/tag/v1.13.2) and [libE57 tools](http://www.libe57.org/download.html) were used to analyze, design, develop and test this script.

## Background

As part of the [NFDI4Culture](https://nfdi4culture.de/) initiative, efforts are underway to enhance the capabilities of open-source digital preservation software like Archivematica to identify, validate and characterize 3D file formats. This repository provides a script to improve metadata extraction of E57 files in Archivematica, enhancing its 3D content preservation capabilities.

## Related projects

- [DAE Validator for Archivematica](https://github.com/JoergHeseler/dae-validator-for-archivematica)
- [E57 Validator for Archivematica](https://github.com/JoergHeseler/e57-validator-for-archivematica)
- [glTF Validator for Archivematica](https://github.com/JoergHeseler/gltf-validator-for-archivematica)
- [Mesh Samples for Preservation Testing](https://github.com/JoergHeseler/mesh-samples-for-preservation-testing)
- [Point Cloud Samples for Digital Preservation Testing](https://github.com/JoergHeseler/point-cloud-samples-for-preservation-testing)
- [Siegfried Falls Back on Fido Identifier for Archivematica](https://github.com/JoergHeseler/siegfried-falls-back-on-fido-identifier-for-archivematica)
- [STL Cleaner](https://github.com/JoergHeseler/stl-cleaner)
- [STL Metadata Extractor for Archivematica](https://github.com/JoergHeseler/stl-metadata-extractor-for-archivematica)
- [STL Validator for Archivematica](https://github.com/JoergHeseler/stl-validator-for-archivematica)
- [X3D Validator for Archivematica](https://github.com/JoergHeseler/x3d-validator-for-archivematica)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

Special thanks to the colleagues from the SLUB Dresden, specifically from the Infrastructure and Long-Term Availability division, for their support and valuable feedback during the development.

## Imprint

[NFDI4Culture](https://nfdi4culture.de/) – Consortium for Research Data on Material and Immaterial Cultural Heritage.  
Funded by the German Research Foundation (DFG), Project No. [441958017](https://gepris.dfg.de/gepris/projekt/441958017).

**Author**: [Jörg Heseler](https://orcid.org/0000-0002-1497-627X)  
**License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
