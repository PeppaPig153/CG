varying vec3 v_view_direction;
varying vec3 v_normal;
varying vec2 v_texture_coordinate;

varying vec4 vertex_color;
uniform vec3 lightPos;
uniform vec3 lightColor;
uniform float lightStrength;
uniform vec3 camera_pos;


void main(){
    vec4 point = gl_Vertex;
	float specular_strength = 1.0;

	// vertex_color = gl_Color;
	// vec4 point = gl_Vertex;
	// gl_Position = gl_ModelViewProjectionMatrix * point;
	vec4 color = gl_Color;

	vec3 ambient = lightStrength * lightColor;
	vec3 Normal = gl_Normal;
	vec3 norm = normalize(Normal);
	//norm = normalize(norm);
	vec3 FragPos = vec3(point.x, point.y, point.z);
	vec3 lightDir = normalize(lightPos - FragPos);
	if(norm[0] * lightDir[0] + norm[1] * lightDir[1] + norm[2] * lightDir[2] > 0.0){
		norm = vec3(-norm[0], -norm[1], -norm[2]);
	}
	float diff = max(dot(norm, lightDir), 0.0);
	vec3 diffuse = diff * lightColor;

	vec3 view_dir = normalize(camera_pos - vec3(point));
	vec3 reflect_dir = reflect(-lightDir, norm);
	float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 16.0);
	vec3 specular = specular_strength * spec * lightColor;

	vec3 result = (ambient + diffuse + specular) * vec3(color);
	color = vec4(result, color[3]);
	vertex_color = color;
	if(norm[0] == 0.0 && norm[1] == 0.0 && norm[2] == 0.0){
		vertex_color = vec4(0.0, 0.0, 0.0, 1.0);
	}

	if (abs(point.x) == 1.0 || abs(point.y) == 1.0){
		point.w = 0.0;
	}
	// else{
	// 	float t1 = norm[0] * camera_pos[0] + norm[1] * camera_pos[1] + norm[2] * camera_pos[2];
	// 	float t2 = norm[0] * lightPos[0] + norm[1] * lightPos[1] + norm[2] * lightPos[2];
	// 	float p1 = sqrt(camera_pos[0] * camera_pos[0] + camera_pos[1] * camera_pos[1] + camera_pos[2] * camera_pos[2]);
	// 	float p2 = sqrt(lightPos[0] * lightPos[0] + lightPos[1] * lightPos[1] + lightPos[2] * lightPos[2]);
	//
	// 	if(abs(abs(t1 / p1) - abs(t2 / p2)) < 0.5){
	// 		vertex_color = vec4(1.0, 1.0, 1.0, 1.0);
	// 	}
	//
	// }
	gl_Position = gl_ModelViewProjectionMatrix * point;

	// v_texture_coordinate = gl_MultiTexCoord0.xy;
	// v_view_direction = -gl_ModelViewMatrix[3].xyz;
	// v_normal = gl_NormalMatrix * gl_Normal;
}
