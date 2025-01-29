# Puppyteer

Puppyteer is a project I started because I'm not good at drawing I don't like AI art and I want to be a PNG YouTuber with a cartoon character.  

It's designed to let the user combine different assets rotate and scale and pin them together, you can do this stuff with any image editor,
but I made it easier for my use case.    

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

There is now release yet so you'll have to go set up your environment as you know: 

1. Download or Clone.
```bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git
```

2. Go ahead and install the requirements witch are pygame and pywin32.
```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

If you give it a little patient you'll get how to use it quick.

the flow will be something like this:

1. You load the folder with all of your character's assets.
2. Rotate, scale, flip, and, mash them together until you get something you like.
3. Most controls are with the mouse you use shift and ctrl to change what happens.
4. export the images you make and save the presets you made if you like.

## Features

- Pinning layers:
  - On each other choose the layer you want to pin.
  - Press the pin button.
  - Choose the layer you want to pin it to.
  - You will still be able to move the pined layer, but it'll move with the layer it's been pined to.  
  

- Presets:
  - If you want to keep how some layers look together hide the rest and press the plus button.
  - you can now load that look whenever you want.
  - use right click to remove presets.


- Merge:
  - If you liked presets but want something more permanent you can use merge.
  - Same as for the presets only this time press the colorful button on the bottom.
  - Now you have a new layer it's also saved into the folder you loaded.


- Scale:
  - Make sure the pointer is within the layer's box using the wheel will make it scale up or down.  


- Rotate:
  - Same as scaling just be sure to keep pressing ctrl.


- Mirror:
  - There are three buttons for this it for how you like your symmetry.
  - You can rotate or scale them and the copy will mirror it.
  - You control the distance between the image and its mirror with the wheel while holding shift.
  - You can also rotate both of them around the center of the original by holding both shift and ctrl using the wheel.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the [MIT License](LICENSE). Please see the `LICENSE` file for more details.