import re

def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)

def in2post(exp_string):
	output_stack = []
	tmp_stack = []
	while(len(exp_string) > 0):
		ch = exp_string[:1]

		if ch == '(':
			tmp_stack.append(ch)
			exp_string = exp_string[1:]
		elif ch == '+' or ch == '-':
			if len(tmp_stack) > 0:
				while tmp_stack[len(tmp_stack)-1] == '*' or tmp_stack[len(tmp_stack)-1] == '/':
					output_stack.append(tmp_stack[len(tmp_stack)-1])
					tmp_stack.pop()
					if len(tmp_stack) == 0:
						break
			tmp_stack.append(ch)
			exp_string = exp_string[1:]
		elif ch == '*' or ch == '/':
			tmp_stack.append(ch)
			exp_string = exp_string[1:]
		elif ch == ')':
			while tmp_stack[len(tmp_stack)-1] != '(':
				output_stack.append(tmp_stack[len(tmp_stack)-1])
				tmp_stack.pop()
			tmp_stack.pop()
			exp_string = exp_string[1:]
		else:
			val_name = ""
			while exp_string[:1].isalnum():
				val_name += exp_string[:1]
				exp_string = exp_string[1:]
			output_stack.append(val_name)
	while len(tmp_stack) > 0:
		output_stack.append(tmp_stack[len(tmp_stack)-1])
		tmp_stack.pop()
	return output_stack

class LSystem3D:
	l_string = ""
	state_stack = []
	rules = []
	polygon_edges = []
	constants = {}
	tropism_vector = (0,0,0)

	def __init__(self,axiom, rule_list,constant_dict,tropism):
		self.l_string = axiom
		self.tropism_vector = tropism

		for rule in rule_list:
			self.rules.append(rule)

		self.constants = constant_dict

	def set_axiom(self,axiom_string):
		l_string = axiom_string

	def insert_rule(self,predecessor,successor):
		self.rule_dict.append((predecessor,successor))

	def insert_rule_list(self,rule_list):
		for rule in rule_list:
			self.rules.append(rule)

	def iterate(self):
		rep_dict = {}
		for rule in self.rules:
			if rule[0].find('(') == -1:
				# index = 0
				# while index < len(self.l_string):
				# 	index = self.l_string.find(rule[0],index)
				# 	if index == -1:
				# 		break
				# 	# print(rule[0]+" found at",index)
				# 	replace_pos.append(index)
				# 	index += len(rule[0])
				# self.replace_ch(replace_pos,rule[0],rule[1])
				rep_dict[rule[0]] = rule[1]
				# self.l_string = self.l_string.replace(rule[0],rule[1])
			else:
				func_name = rule[0][:rule[0].find("(")]
				tmp_var = ""
				var_list = []
				val_list = []
				for index in range(rule[0].find("(")+1,len(rule[0])):
					if rule[0][index] == ',':
						var_list.append(tmp_var)
						tmp_var = ""
					elif rule[0][index] == ')':
						var_list.append(tmp_var)
						break
					else:
						tmp_var = tmp_var + rule[0][index]
				# print(func_name,var_list)

				index = 0
				while index < len(self.l_string):
					index = self.l_string.find(func_name,index)
					if index == -1:
						break
					index += len(func_name)+1
					tmp_var = ""
					val_list = []
					while True:
						if self.l_string[index] == ',':
							val_list.append(tmp_var)
							tmp_var = ""
						elif self.l_string[index] == ')':
							val_list.append(tmp_var)
							index += 1
							break
						else:
							tmp_var = tmp_var + self.l_string[index]
						index += 1
					# print(var_list,val_list)
					rule0_cpy = rule[0]
					rule1_cpy = rule[1]
					for i in range(len(var_list)):
						rule0_cpy = rule0_cpy.replace(var_list[i],val_list[i])
						rule1_cpy = rule1_cpy.replace(var_list[i],val_list[i])

					rep_dict[rule0_cpy] = rule1_cpy
					# self.l_string = self.l_string.replace(rule0_cpy,rule1_cpy)
					# index += 1
					# print(index,self.l_string)
					# break
					# print(index)
		# print(rep_dict)
		self.l_string = multiple_replace(self.l_string,rep_dict)

	def calculate_expression(self,exp_string):
		num_stack = []
		print(exp_string)
		post_list = in2post(exp_string)
		# print(post_list)
		for element in post_list:
			if element.isalpha():
				num_stack.append(float(self.constants[element]))
			elif element.isnumeric():
				num_stack.append(float(element))
			elif element == '+':
				val2 = num_stack[len(num_stack)-1]
				val1 = num_stack[len(num_stack)-2]
				num_stack.pop()
				num_stack.pop()
				num_stack.append(val1+val2)
			elif element == '-':
				val2 = num_stack[len(num_stack)-1]
				val1 = num_stack[len(num_stack)-2]
				num_stack.pop()
				num_stack.pop()
				num_stack.append(val1-val2)
			elif element == '*':
				val2 = num_stack[len(num_stack)-1]
				val1 = num_stack[len(num_stack)-2]
				num_stack.pop()
				num_stack.pop()
				num_stack.append(val1*val2)
			elif element == '/':
				val2 = num_stack[len(num_stack)-1]
				val1 = num_stack[len(num_stack)-2]
				num_stack.pop()
				num_stack.pop()
				num_stack.append(val1/val2)
		return num_stack[0]

	def calculate_edge(self):
		turtles = [(0,0,0),(0,0,0),1]
		for index in range(len(self.l_string)):
			if self.l_string[index] == '+' or  self.l_string[index] == '-':
				index+=1
				tmp_string = ""
				while self.l_string[index] != ')':
					tmp_string += self.l_string[index]
					index+=1
				tmp_string+=')'
				value = self.calculate_expression(tmp_string)
				


# print("2222A1111"[:4]+"2222A1111"[-3:])
# print(in2post("a-2*(43*aj)"))
tree = LSystem3D("!(1)F(200)/(45)A"
	,[("A","!(Vr)F(50)[&(a)F(50)A]/(d1)[&(a)F(50)A]/(d2)[&(a)F(50)A]")
	,("F(l)","F(l*Lr)"),("!(w)","!(w*Vr)")]
	,{"d1":94.74,"d2":132.63,"a":18.95,"lr":1.109,"Vr":1.109}
	,(0.0,-1.0,0.0))
# print(tree.l_string)
tree.iterate()
tree.calculate_edge()
print(tree.l_string)
# tree.insert_rule_list([(1,2)])