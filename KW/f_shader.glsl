varying vec4 vertex_color;
varying vec3 vertex_norm;
varying vec3 vertex_pos;

uniform vec3 lightPos;
uniform vec3 camera_pos;
uniform vec3 lightColor;






void main() {
	vec3 m_ambiant = vec3(0.0, 0.1, 0.06);
	vec3 m_diffuse = vec3(0.0, 0.50980392, 0.50980392);
	vec3 m_specular = vec3(0.50196078, 0.50196078, 0.50196078);
	m_ambiant = lightColor;
	m_diffuse = lightColor;
	m_specular = lightColor;
	float m_shininess = 256.0;
	float alpha = vertex_color[3];
	// Ambient
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse
    vec3 norm = normalize(vertex_norm);
    vec3 lightDir = normalize(lightPos - vertex_pos);
	if(norm[0] * lightDir[0] + norm[1] * lightDir[1] + norm[2] * lightDir[2] < 0.0){
		norm = vec3(-norm[0], -norm[1], -norm[2]);
	}
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * m_diffuse;

    // Specular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(camera_pos - vertex_pos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), m_shininess);
    vec3 specular = specularStrength * spec * m_specular;
	if(vertex_color[0] == 0.0 && vertex_color[1] == 1.0 && vertex_color[2] == 0.0){
		// specular = vec3(0.0, 0.0, 0.0);
		// diffuse = vec3(0.0, 0.0, 0.0);
		// result = vec3(vertex_color);
	}
    vec3 result = (ambient + diffuse + specular) * vec3(vertex_color);

    gl_FragColor = vec4(result, alpha);
    // gl_FragColor = vertex_color;
}
