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
// FILE: sharpness.glsl
// AUTHOR(S): Noah Rahm
// PURPOSE: Adjust the sharpness of an RGBA image
// ----------------------------------------------------------------------------

#version 330

uniform sampler2D image;
out vec4 out_color;
uniform float sharpnessValue;

void main() {
    vec4 color = texelFetch(image, ivec2(gl_FragCoord.xy), 0);

    vec3 diffSum = vec3(0.0, 0.0, 0.0);

    for(int xx = -1; xx < 2; ++xx)
    {
        for(int yy = -1; yy < 2; ++yy)
        {
            vec3 dif = color.rgb - texture(image, vec2(.1, .1) + vec2(1.0, 1.0) * vec2(float(xx), float(yy))).rgb;
            diffSum += dif;
        }
    }

    diffSum /= 9.0;

    color.rgb = color.rgb + (sharpnessValue * diffSum);

    out_color = vec4(color.rgb, color.a);
}
