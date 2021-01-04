# Blender4FTC

Blender plugin for simple FTC usage

# **How to install:**
If you already have a Blender4FTC version , head into `Edit > Preferences > Addons`. Find the Blender4FTC addon and remove it.
Go to blender, go to `Edit > Preferences > Addons`. Click `Install`, navigate to the downloaded zip folder and double click on it, and press the check box next to the newly installed addon.

# Panel Info

In the 3D Viewport there are a variety of panels inside of the Blend4FTC tab.

**MaterialLib**
The MaterialLib panel holds functionality for the material library and SmartShade.
You can click "Import Default MaterialLib" to import the embedded material library stored in the addons file. You may also import custom material libraries from other blend files.
SmartShade uses the names of parts imported to appropriately assign materials to goBILDA parts if possible.
The selected material can be assigned to selected objects in the 3dviewport using the assign button.

**Scene Management**
The Scene Management panel is designed to optimize and configure render settings for generic renders.
Performance maps to samples, theme mapping to color space and exposure.

**Compositing Effects**
All of the compositing effects are compiled into a compositing tree on use of `Save and Apply`
Compositing effects include:

`Void Color` - Color of transparent space/the void
`Lens Distortion` - Slight lens distortion and fit
`Denoising Fac` - Factor that the result image is mixed with a denoised image
`Contrast` - Composited contrast modifier(0 is normal)
`Brightness` - Composited brightness modifier(0 is normal)

**Scene Presets**
The Scene Presets panel is designed to provide basic lighting configurations and scenes.

`Make Field` - Imports full field from the embedded material library inside of the addon.
`Basic World & Lighting` - Enables AO & imports embedded HDRI inside of the addon to the world.
`VPanel` - VPanel is a configurable plain background. Use VPanel Color and Roughness to adjust the look of it. `NOTE: VPanel will NOT work without the default material library being imported`

**Material Workshop**
The material workshop is designed to expose properties of materials so that they can be easily configured and edited.
To configure a material, click on it in the MaterialLib tab. Exposed properties will now be editable, and the ability to rename and duplicate the selected material.
You can add your own exposed properties to the Material Workshop tab by renaming nodes in the shader editor to include the prefix "`P] `"

# Downloads
Downloads can be found in the releases section.

# Development
Sadly, GitHub does not allow file uploads of over 100mb and the MaterialLibrary files are over 200mb of data.
In order to set up a development environment, clone this repo locally, and download a release. You can extract the release and use the HDR and `packs` folder from there in your development environment. 
