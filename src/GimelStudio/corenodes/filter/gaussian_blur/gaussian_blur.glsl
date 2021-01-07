// THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
// ----------------------------------------------------------------------------
// Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// FILE: gaussian_blur.glsl
// AUTHOR(S): Noah Rahm
// PURPOSE: Blurs an RGBA image with a 3x3 Gaussian Blur
// ----------------------------------------------------------------------------

#version 330

uniform sampler2D image;
out vec4 out_color;
uniform float blurValue;

void main() {
    vec4 color = texelFetch(image, ivec2(gl_FragCoord.xy), 0);

    int y;
    int x;

    for(y < -1; y < 2; ++y)
    {
        for(x < -1; x < 2; ++x)
        {
            vec2 offset = vec2(float(x), float(y)) * blurValue;
            color.rgb += color.rgb + offset; //texture2D(image, color + offset);
        }
    }
    color.rgb *= 1.0 / 10.0;

    out_color = vec4(color.rgb, blurValue);
}
