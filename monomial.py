# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:10:33 2022

@author: books
"""
import math

class Monomial():
    #Need to add better handling of printing
    #Need to add scalar multiplication
    
    def order_type():
        return Polynomial.order_type()
    
    def set_order_type(new_order):
        Polynomial.set_order_type(new_order)
    
    subscript_list=('₀','₁','₂','₃','₄','₅','₆','₇','₈','₉')
    superscript_list=('⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹')
    
    
    def __init__(self, coefficient=1, exponent_tuple=(0,)):
        self.coefficient=coefficient
        self.exponents=exponent_tuple
        self.num_vars=len(exponent_tuple)
        self.degree=sum(exponent_tuple)
        
    def __str__(self):
        string=str(self.coefficient)
        for index, exponent in enumerate(self.exponents):
            if exponent!=0:
                string+="x"+self.subscript_list[index+1]+self.superscript_list[exponent]
        return string
    
    def __repr__(self):
        return self.__str__()
    
    def __mul__(self, factor2):
        if len(self.exponents)!=len(factor2.exponents):
            raise TypeError('Monomials are not defined on same number of variables.')
        
        exponent_list=[]
        for i in range(len(self.exponents)):
            exponent_list.append(self.exponents[i]+factor2.exponents[i])
        
        product_coefficient=self.coefficient*factor2.coefficient
        
        return Monomial(coefficient=product_coefficient, exponent_tuple=tuple(exponent_list))
    
    def __add__(self, mon2):
        if self.exponents!=mon2.exponents:
            raise TypeError('Cannot add monomials with different exponents.')
        
        sum_coefficient=self.coefficient+mon2.coefficient
        return Monomial(coefficient=sum_coefficient, exponent_tuple=self.exponents)
    
    def __truediv__(self, mon2):
        if self.coefficient % mon2.coefficient==0:
            div_coef=self.coefficient//mon2.coefficient
        else:
            div_coef=self.coefficient/mon2.coefficient
        div_exponents=()
        for exp1, exp2 in zip(self.exponents, mon2.exponents):
            div_exponents+=(exp1-exp2,)
        if min(div_exponents)<0:
            raise ValueError('Division results in negative exponents.')
        return Monomial(div_coef, div_exponents)
    
    def __eq__(self, mon2):
        return_value=None
        if self.coefficient==mon2.coefficient and self.exponents==mon2.exponents:
            return_value=True
        else:
            return_value=False
        return return_value
    
    def __ge__(self, mon2):
        return_value=None
        order_type=Monomial.order_type()
        if order_type=='lex':
            for index in range(len(self.exponents)):
                if self.exponents[index]>=mon2.exponents[index]:
                    return_value=True
                    break
                elif self.exponents[index]<=mon2.exponents[index]:
                    return_value=False
                    break
            if return_value==None:
                if self.coefficient>=mon2.coefficient:
                    return_value=True
                else:
                    return_value=False
        elif order_type=='deglex':
            if self.degree>mon2.degree:
                return_value=True
            elif self.degree<mon2.degree:
                return_value=False
            else:
                Monomial.set_order_type('lex')
                return_value= self>=mon2
                Monomial.set_order_type('deglex')
        elif order_type=='degrevlex':
            if self.degree>mon2.degree:
                return_value=True
            elif self.degree<mon2.degree:
                return_value=False
            else:
                Monomial.set_order_type('lex')
                rev_mon1=Monomial(self.coefficient, self.exponents[::-1])
                rev_mon2=Monomial(mon2.coefficient, mon2.exponents[::-1])
                return_value= not rev_mon1>=rev_mon2
                Monomial.set_order_type('degrevlex')
        return return_value
    
    def __lt__(self, mon2):
        return_value=not self>=mon2
        return return_value
    
    def __gt__(self, mon2):
        return self>=mon2 and self!=mon2
    
    def __le__(self, mon2):
        return self==mon2 or not self>=mon2
    
    def to_poly(self):
        return Polynomial([self])
    
    def subscript(integer):
        sub_string=''
        for k in list(str(integer)):
            sub_string+=Monomial.subscript_list[int(k)]
        return sub_string
    
    def superscript(integer):
        sup_string=''
        for k in list(str(integer)):
            sup_string+=Monomial.superscript_list[int(k)]
        return sup_string
    
    def zero(num_vars=1):
        exponent_tuple=()
        for i in range(num_vars):
            exponent_tuple+=(0,)
        return Monomial(coefficient=0, exponent_tuple=exponent_tuple)
    
    def lcm(mon1, mon2):
        lcm_coefficient=math.lcm(mon1.coefficient, mon2.coefficient)
        lcm_exponents=()
        for exp1, exp2 in zip(mon1.exponents, mon2.exponents):
            lcm_exponents+=(max(exp1, exp2),)
        return Monomial(coefficient=lcm_coefficient, exponent_tuple=lcm_exponents)
    
    def gcd(mon1, mon2):
        return mon1*mon2/Monomial.lcm(mon1, mon2)
    
            
    
    
    
    
class Polynomial():
    _order_type='lex'
    
    # @property
    # def order_type():
    #     return order_type
    
    # @order_type.setter
    # def order_type(new_order):
    #     if new_order=='lex':
    #         order_type='lex'
    #     elif new_order=='deglex':
    #         order_type=='deglex'
    #     elif new_order=='degrevlex':
    #         order_type='degrevlex'
    #     else:
    #         print('Please use a valid order type.')
    
    def set_order_type(new_order):
        if new_order=='lex':
            order_type='lex'
        elif new_order=='deglex':
            order_type='deglex'
        elif new_order=='degrevlex':
            order_type='degrevlex'
        else:
            print('Please use a valid order type.')
            order_type=None
        if order_type!=None:
            Polynomial._order_type=order_type
        
    def order_type():
        return Polynomial._order_type
    
    def __init__(self, terms_list):
        self.terms=terms_list
        
    def simplify(self):
        terms_list=self.terms
        simplified_list=[]
        indices_appended=[]
        for i, mon1 in enumerate(terms_list):
            if i in indices_appended:
                continue
            match=False
            for j, mon2 in enumerate(terms_list[i+1:], start=i+1):
                if mon1.exponents==mon2.exponents:
                    match=True
                    indices_appended.append(i)
                    indices_appended.append(j)
                    simplified_list.append(mon1+mon2)
            if match==False:
                indices_appended.append(i)
                simplified_list.append(mon1)
        for term in simplified_list:
            if term.coefficient==0:
                simplified_list.remove(term)
        return Polynomial(simplified_list)
                
        
    def __add__(self, poly2): #Need to fix. Excludes terms from poly2 which have no matching term in poly1
        union_list=self.terms+poly2.terms
        return Polynomial(union_list).simplify()
    
    def __sub__(self, poly2):
        poly3_list=[]
        for term in poly2.terms:
            poly3_list.append(Monomial(-1*term.coefficient, term.exponents))
        poly3=Polynomial(poly3_list)
        return self+poly3
        
    
    def __str__(self):
        string=''
        for term in self.terms:
            string+=str(term)+'+'
        string=string.strip('+')
        if string=='':
            string='0'
        return string
    
    def __repr__(self):
        return self.__str__()
    
    def __mul__(self, poly2):
        polynomials=[]
        for mon1 in self.terms:
            for mon2 in poly2.terms:
                polynomials.append(Polynomial([mon1*mon2]))
        poly_sum=polynomials[0]
        for poly in polynomials[1:]:
            poly_sum=poly_sum+poly
        return poly_sum
    
    def __truediv__(self, mon1):
        if not isinstance(mon1, Monomial):
            raise Exception('Polynomial divison only supported for Monomial divisor.')
        quotient_terms=[]
        for term in self.terms:
                quotient=term/mon1
                quotient_terms.append(quotient)
        return Polynomial(quotient_terms)
    
    def __eq__(self, poly2):
        poly1=self.simplify()
        poly2=poly2.simplify()
        if len(poly1.terms)!=len(poly2.terms):
            return False
        for term1 in poly1.terms:
            has_match=False
            for term2 in poly2.terms:
                if term1==term2:
                    has_match=True
            if has_match==False:
                return False
        return True
    
    def leading_term(self):
        greatest_term=self.terms[0]
        for term in self.terms:
            if term>greatest_term:
                greatest_term=term
        return greatest_term
    
    def leading_coef(self):
        return self.leading_term().coefficient
    
    def leading_mon(self):
        leading_term=self.leading_term()
        return Monomial(1, leading_term.exponents)
    
    def __gt__(self, poly2):
        if self.leading_term()>poly2.leading_term():
            return True
        else:
            return False
    
    def __lt__(self, poly2):
        if self!=poly2 and not self>poly2:
            return True
        else:
            return False
        
    def __ge__(self, poly2):
        if self>poly2 or self==poly2:
            return True
        else:
            return False
        
    def __le__(self, poly2):
        if not self>poly2:
            return True
        else:
            return False
        
    def sort(self, descending=True):
        terms=self.simplify().terms
        terms.sort(reverse=descending)
        return Polynomial(terms)
        
        
    def is_reducible_by(self, g):
        f=self.simplify()
        h=g.leading_mon()
        for term in f.terms:
            try:
                term/h
                return True
            except:
                pass
        return False
    
    def is_reducible_by_set(self, G):
        for g in G:
            if self.is_reducible_by(g):
                return True
            else:
                pass
        return False
        
    def reduce_one(self, g):
        if not self.is_reducible_by(g):
            raise Exception(str(self)+' is not reducible by '+str(g))
        f=self.sort()
        h=g.leading_term()
        for term in f.terms:
            try:
                quotient=term/h
                break
            except:
                pass
        return f-quotient.to_poly()*g
    
    def reduce_one_set(self, G):
        if not self.is_reducible_by_set(G):
            raise Exception(str(self)+' is not reducible by '+str(G))
        f=self.sort()
        G_sorted=G[:]
        G_sorted.sort(reverse=True)
        for g in G_sorted:
            try:
                f=f.reduce_one(g)
                break
            except:
                pass
        return f
        
    
    def reduce_complete(self, G):
        f=self
        while f.is_reducible_by_set(G):
            f=f.reduce_one_set(G)
        return f
        
    def buchberger(F):
        G=F[:]
        for f1 in G:
            for f2 in G:
                g1=f1.leading_mon()
                g2=f2.leading_mon()
                a=Monomial.lcm(g1, g2).to_poly()
                S=(a*f1)/g1-(a*f2)/g2
                S_reduced=S.reduce_complete(G).simplify()
                if S_reduced.terms!=[]:
                    G.append(S_reduced)
        return G
    
    def check_groebner_basis(F,G):
        for f in F:
            f_reduced=f.reduce_complete(G).simplify()
            if f_reduced.terms==[]:
                pass
            else:
                return False
        return True
        
#%%

mon1=Monomial(1, (1,2,1))
mon2=Monomial(2, (3,0,0))
mon3=Monomial(3, (0,1,1))

poly1=Polynomial([mon1, mon2])
       
        
    

            
        
        