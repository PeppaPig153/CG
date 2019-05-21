varying vec4 vertex_color;


void main() {
    gl_FragColor = vertex_color;
}

// uniform samplerCube texture_reflection;
// uniform sampler2D texture_iridescence;
// uniform sampler2D texture_noise;
//
// varying vec3 v_view_direction;
// varying vec3 v_normal;
// varying vec2 v_texture_coordinate;
//
// const float noise_strength = 0.5;
//
// void main(void)
// {
//    vec3 n_normal = normalize(v_normal);
//    vec3 n_wiew_direction = normalize(v_view_direction);
//    vec3 n_reflection = normalize(reflect(n_wiew_direction, n_normal));
//
//    vec3 noise_vector = (texture2D(texture_noise, v_texture_coordinate).xyz - vec3(0.5)) * noise_strength;
//
//    float inverse_dot_view = 1.0 - max(dot(normalize(n_normal + noise_vector), n_wiew_direction), 0.0);
//    vec3 lookup_table_color = texture2D(texture_iridescence, vec2(inverse_dot_view, 0.0)).rgb;
//
//    gl_FragColor.rgb = textureCube(texture_reflection, n_reflection).rgb * lookup_table_color * 2.5;
//    gl_FragColor.a = 1.0;
// }
//
// uniform samplerCube cubeMap;
//
// varying vec3 ViewDirection;
// varying vec3 Normal;
//
// const float mother_pearl_brightness = 1.5;
//
// #define MOTHER_PEARL
//
// void main( void )
// {
//    vec3  fvNormal         = normalize(Normal);
//    vec3  fvViewDirection  = normalize(ViewDirection);
//    vec3  fvReflection     = normalize(reflect(fvViewDirection, fvNormal));
//
// #ifdef MOTHER_PEARL
//    float view_dot_normal = max(dot(fvNormal, fvViewDirection), 0.0);
//    float view_dot_normal_inverse = 1.0 - view_dot_normal;
//
//    gl_FragColor = textureCube(cubeMap, fvReflection) * view_dot_normal;
//    gl_FragColor.r += mother_pearl_brightness * textureCube(cubeMap, fvReflection + vec3(0.1, 0.0, 0.0) * view_dot_normal_inverse) * (1.0 - view_dot_normal);
//    gl_FragColor.g += mother_pearl_brightness * textureCube(cubeMap, fvReflection + vec3(0.0, 0.1, 0.0) * view_dot_normal_inverse) * (1.0 - view_dot_normal);
//    gl_FragColor.b += mother_pearl_brightness * textureCube(cubeMap, fvReflection + vec3(0.0, 0.0, 0.1) * view_dot_normal_inverse) * (1.0 - view_dot_normal);
// #else
//    gl_FragColor = textureCube(cubeMap, fvReflection);
// #endif
// }
