uniform vec3 lightPos;
uniform vec3 lightColor;
uniform vec3 objectColor;
uniform vec3 scale;
uniform vec3 centre;
uniform float lightStrength;
varying vec4 vertex_color;
uniform float freq;
uniform float angle_1s;
uniform float angle_1c;
uniform float angle_2s;
uniform float angle_2c;

void main(){
    vec4 point = gl_Vertex;

	vertex_color = vec4(objectColor, 1.0);
	if(!(
	 	((point.x+point.y+point.z)==1.0
			&& (point.x==1.0
				|| point.y==1.0
				|| point.z==1.0
			)
		)
		// || (point.x == 0.0 && point.y == 0.0 && point.z == 0.0)
	)){
		if(!(point.x == 0.0 && point.y == 0.0 && point.z == 0.0)){
		mat4 scale_matrix = mat4(
			scale[0], 0.0, 0.0, 0.0,
			0.0, scale[1], 0.0, 0.0,
			0.0, 0.0, scale[2], 0.0,
			0.0, 0.0, 0.0, 1.0
		);

		float radius = sqrt(point.x * point.x + point.y * point.y);
		point.z = point.z + sin(radius * freq) * 0.1;
		point = scale_matrix * point;
		float cosx = cos(radius * freq);
		float r = sqrt(cosx * cosx / (1.0 + cosx * cosx));
		float norm_x = r * point.x / radius;
		float norm_y = r * point.y / radius;
		float norm_z = 1.0 / sqrt(1.0 + cosx * cosx);
		vec3 norm = vec3(norm_x, norm_y, norm_z);
		mat4 rotation_matrix = mat4(
			angle_2c, 0.0, -angle_2s, 0.0,
			-angle_1s * angle_2s, angle_1c, -angle_1s * angle_2c, 0.0,
			angle_2s * angle_1c, angle_1s, angle_1c * angle_2c, 0.0,
			0.0, 0.0, 0.0, 1.0
		);

		point = rotation_matrix * point;
		point = point + vec4(centre, 0.0);











		vec4 color = vec4(objectColor, 1.0);




		vec3 ambient = lightStrength * lightColor;
		// vec3 Normal = norm;
		// vec3 Normal = gl_Normal;
		// vec3 norm = normalize(Normal);
		norm = normalize(norm);
		vec3 FragPos = vec3(point.x, point.y, point.z);
		vec3 lightDir = normalize(lightPos - FragPos);
		float diff = max(dot(norm, lightDir), 0.0);
		vec3 diffuse = diff * lightColor;
		vec3 result = (ambient + diffuse) * objectColor;
		color = vec4(result, 1.0);
		vertex_color = color;
	}
	}
	else{
		point.w = 0.0;
		vertex_color = gl_Color;
	}
	if(point.x == 0.0 && point.y == 0.0 && point.z == 0.0){
		vertex_color = gl_Color;
		// color = vec4(0.0, 0.0, 0.0, 1.0);
	}

	gl_Position = gl_ModelViewProjectionMatrix * point;

}
