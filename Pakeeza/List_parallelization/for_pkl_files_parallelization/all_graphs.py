import networkx as nx
import numpy as np
import os
#from mpi4py import MPI
#import pandas as pd
import copy
#import random
import itertools
from itertools import combinations
#from itertools import permutations
import pickle
# from Get_compositions import *
import sys
import ast


##########FUNCTIONS########################################################################
def graph_label(edge_list):
    nodes=list(set([item for t in edge_list for item in t]))
    nodes.sort()
    ALL_COMBS=[]
    all_combs=list(itertools.permutations(nodes)) #1
    for i in all_combs:
        j=list(i)
        new_list=[]
        for z in edge_list:
            a_=j.index(z[0])+1                    #2
            b_=j.index(z[1])+1
            new_list.append((a_,b_))
        new_list.sort()
        ALL_COMBS.append(new_list)
    ALL_COMBS.sort()                              #3
    return(ALL_COMBS[0])                          #4


##############################


##test if the graph has multiple possible "start" nodes [nodes with 0 in-edges] - if yes, don't test this graph because the graph is essentially reduced to another topology with a lesser compartment
#if one such start nodes is the ER, the other start node with no directed paths to the labeled ER would have no "incoming" cargo and is essentially a null compartment
def test_graph_and_possible_ER(edge_list,no_of_coats):    
    G = nx.DiGraph()
    G.add_edges_from(edge_list)

    compartments=list(set([item for t in edge_list for item in t]))
    compartments.sort()

    roots=[]

    for i in compartments:

        if len(list(G.in_edges(i)))==0:
            roots.append(i)

    if len(roots)>1:
        x=0
        possible_ER=[]


    elif len(roots)==0:
        x=1
        possible_ER=compartments


    else:
        x=1
        possible_ER=roots
        
        
    #no_of_coats
    
    unique_edges=list(set(edge_list))
    counts=[]
    for i in unique_edges:
        c=edge_list.count(i)
        counts.append(c)
   
    y=0
    #print(no_of_coats,max(counts),len(edge_list))
    if max(counts) <= no_of_coats <= len(edge_list):
        y=1
    
    z=x&y
    #print(z)

    return z,possible_ER



def list_of_cargos_(no_of_coats):
    cargo=[]
    cargo_list=list(itertools.product([0, 1], repeat=no_of_coats))
    #for i in cargo_list:
        #print(i)
    for i in range(len(cargo_list)):
        cargo.append('c'+str(i+1))
    return cargo

#List of n coats
def get_coat_list(no_of_coats):
    coat_list=[]
    c=0
    for i in range(no_of_coats):
        c=c+1
        coat_list.append('a'+str(c))
    return coat_list


#All ways of labeling the edges with n coats    
def coat_labels(no_of_coats,edge_list):
    coat_list=[]
    c=0
    for i in range(no_of_coats):
        c=c+1
        coat_list.append('a'+str(c))
    
    nodes=list(set([item for t in edge_list for item in t]))
    node_combs=[]
    for i in nodes:
        for j in nodes:
            node_combs.append((i,j))
    edge_list.sort()
    final_list=[]
    node_combs_=[]
    for i in node_combs:
        
        counts=0
        
        for j in edge_list:
            if j[0]==i[0] and j[1]==i[1]:
                counts=counts+1
        if counts>0:
            node_comb_list=list(combinations(coat_list, counts))
            final_list.append(node_comb_list)
            node_combs_.append(i)
        
        
   
    fin_combs=list(itertools.product(*final_list))
   
    fin_combs_=[]
    for i in fin_combs:
        j=[element for tupl in i for element in tupl]
        fin_combs_.append(j)
        
    return(fin_combs_)


def list_of_cargos(no_of_coats):
    cargo=[]
    cargo_list=list(itertools.product([0, 1], repeat=no_of_coats))
    #print(cargo_list)
    for i in range(len(cargo_list)):
        cargo.append('c'+str(i+1))
    return cargo


def list_of_cargo_sets(edge_list,coat_label,no_of_coats):
    c=0
    cargo_coat=cargo_sets(no_of_coats)
    cargo_sets_list=[]
    for i in edge_list:
        j=coat_label[c]
        cargo_sets_list.append(cargo_coat[j])
        c=c+1
    return cargo_sets_list

def cargo_sets(no_of_coats):
    cargo_coat={}
    cargo_list=np.array(list(itertools.product([0, 1], repeat=no_of_coats)))
    
    for i in range(cargo_list.shape[1]):
        coat='a'+str(i+1)
        coat_column=cargo_list[:,i].tolist()
        c=0
        cargo=[]
        for j in coat_column:
            c=c+1
            if j==1:
                cargo.append('c'+str(c))
        cargo_coat[coat]=cargo[:]
    return cargo_coat


def cargo_subgraph(cargo,edge_list,locs):
    c=0
    edges=[]
    for i in locs:
        
        if cargo in i:
            edges.append(edge_list[c])
        c=c+1
    return edges



def get_subgraph_edges(edge_list, ER):
    G = nx.MultiDiGraph()
    G.add_edges_from(edge_list)
    # get the descendants of the root node
    descendants = nx.descendants(G, ER)

    # include the root node in the subgraph
    subgraph_nodes = descendants.union(set([ER]))

    # get the subgraph with the root node and its descendants
    subgraph = G.subgraph(subgraph_nodes)

    # return the edges in the subgraph
    return list(subgraph.edges())

def condensed_cargo_subgraph_new(cargo,edge_list,locs,ER):
   
    sub_edges=cargo_subgraph(cargo,edge_list,locs)
   
    
    sub_nodes = [item for tuple in sub_edges for item in tuple]
    sub_nodes=list(set(sub_nodes))
    
    if ER in sub_nodes:
        
        A=get_subgraph_edges(sub_edges, ER)
      
        G = nx.MultiDiGraph()
        G.add_edges_from(A)
        H = nx.condensation(G)

        #print("condensed")
        #print(H.edges())

        nodes=list(H.nodes())
        #print("H nodes",nodes)
        startnodes = [x for x in H.nodes() if H.in_degree(x)==0]
        #print("startnodes",startnodes)
        endnodes = [x for x in H.nodes() if H.out_degree(x)==0 ]
        #print("endnodes",endnodes)
        all_but_end_nodes=diff(nodes,endnodes)
        #print("all_but_end_nodes",all_but_end_nodes)
        #nodes_data=list(H.nodes.data())
        startnodes_=[]
        endnodes_=[]
        all_but_end_nodes_=[]

        for i in list(H.nodes.data()):
            node_=i[0]
            if node_ in startnodes:
                startnodes_=startnodes_+list(i[1]['members'])
            if node_ in endnodes:
                endnodes_=endnodes_+list(i[1]['members'])
            if node_ in  all_but_end_nodes:
                all_but_end_nodes_= all_but_end_nodes_+list(i[1]['members'])
    else:
        G = nx.MultiDiGraph()
        G.add_edges_from(sub_edges)
        H = nx.condensation(G)

        nodes=list(H.nodes())
        #print("H nodes",nodes)
        startnodes = [x for x in H.nodes() if H.in_degree(x)==0]
        #print("startnodes",startnodes)
        endnodes = [x for x in H.nodes() if H.out_degree(x)==0 ]
        #print("endnodes",endnodes)
        all_but_end_nodes=diff(nodes,endnodes)
        #print("all_but_end_nodes",all_but_end_nodes)
        #nodes_data=list(H.nodes.data())
        startnodes_=[]
        endnodes_=[]
        all_but_end_nodes_=[]

        for i in list(H.nodes.data()):
            node_=i[0]
            if node_ in startnodes:
                startnodes_=startnodes_+list(i[1]['members'])
            if node_ in endnodes:
                endnodes_=endnodes_+list(i[1]['members'])
            if node_ in  all_but_end_nodes:
                all_but_end_nodes_= all_but_end_nodes_+list(i[1]['members'])
                
                
        #Or just set
        #startnodes_=[]
        #endnodes_=[]
        #all_but_end_nodes_=[]
    
    return startnodes_,endnodes_,all_but_end_nodes_,sub_edges



            

def find_edges_of_strongly_connected_nodes(cargo,locs,edge_list,strongly_connected_nodes):
    edges=[]
    edge_numbers=[]
    c=0
    #print("inside fn")
    for i in edge_list:
        #print(i)
        x,y=i
        #print(x)
        #print(y)
        #print("nodes",strongly_connected_nodes)
        #print("locs",locs)
        if x in strongly_connected_nodes and y in strongly_connected_nodes:
            if cargo in locs[c]:
                edges.append(i)
                edge_numbers.append(c)
        c=c+1
    return edges,edge_numbers


def cargo_vesicle_new(cargo,edge_list,edge_numbers,locs,chosen_coat_label):
   
    c=0
    vesicles=[]
    for i in locs:
        
        if cargo in i and c in edge_numbers:
            vesicles.append((chosen_coat_label[c],edge_list[c][0]))
        c=c+1
    return vesicles


def coat_recruiter_solutions(number_of_coats,list_of_vesicle_compositions,list_of_compartment_compositions):
    coat_list=get_coat_list(number_of_coats)
    
    coat_irr_cov={}
    for i in coat_list:
   
        x,col_list_array,col_list_numbers=checking_consistency_coat_recruiter(i,list_of_vesicle_compositions,list_of_compartment_compositions)
   

        if x=='consistent':
            #irr_cov=find_all_covers(col_list_array,col_list_numbers)
            #coat_irr_cov[i]=irr_cov
            coat_irr_cov[i]=col_list_numbers

        else:
            n={}
            #print("inconsistent for coat",i)
            return n
    return coat_irr_cov



def checking_consistency_coat_recruiter(coat,list_of_vesicle_compositions,list_of_compartment_compositions):
    vesicle_coat_list=list(list_of_vesicle_compositions.keys())
    comp_list=list(list_of_compartment_compositions.keys())
    ves_comps=[]
  
    comp_ves_=[]
    comp_no_ves_=[]
    for i in vesicle_coat_list:
        if coat in i:
            comp_ves_.append(list_of_compartment_compositions[i[1]])
            ves_comps.append(i[1])
    for i in comp_list:
        if i not in ves_comps:
            comp_no_ves_.append(list_of_compartment_compositions[i])
        
    
    comp_ves=np.array(comp_ves_)                
    comp_no_ves=np.array(comp_no_ves_)
    
    #print(comp_ves)
    #print(comp_no_ves)

    col_list_numbers=[]
    col_list_array=[]
    for i in range(comp_ves.shape[1]):
            fuse_col=np.count_nonzero(comp_ves[:,i]==1)
            if fuse_col>0:
                if comp_no_ves.shape[0]>0:
                    fuse_non_col=np.count_nonzero(comp_no_ves[:,i]==1)
                    if fuse_non_col==0:
                        col_list_numbers.append(i+1)
                        col_list_array.append(comp_ves[:,i].tolist())
                else:
                    col_list_numbers.append(i+1)
                    col_list_array.append(comp_ves[:,i].tolist())


    col_list_array=np.array(col_list_array).T
   
    if col_list_array.shape[0]==0:
        return "inconsistent",col_list_array,col_list_numbers
    else:
        x=check_if_solution_spans_all(col_list_array)
        return x,col_list_array,col_list_numbers
    
    

def get_vesicle_fusions(edge_list,chosen_coat_label):
    vesicle_fusions={}
    c=0
    for i in edge_list:
        source=i[0]
        coat=chosen_coat_label[c]
        target=[i[1]]
        if (coat,source) in vesicle_fusions.keys():
            target_list=vesicle_fusions[(coat,source)]+target
            vesicle_fusions[(coat,source)]=target_list[:]
        else:
            vesicle_fusions[(coat,source)]=target[:]

        c=c+1
    return vesicle_fusions



def v_a_t_cargo_type_numbers(list_of_vesicle_compositions):
    vesicle=list(list_of_vesicle_compositions.keys())[0]
    v_len=len(list_of_vesicle_compositions[vesicle])
    #comp=list(list_of_compartment_compositions.keys())[0]
    #c_len=len(list_of_compartment_compositions[comp])
    v_snare=[i for i in range(v_len)]
    v_snare_act=[i for i in range(v_len)]
    t_snare=[i for i in range(v_len)]
    
    nums=[]
    for i in v_snare:
       
        for j in v_snare_act:
            
            for k in t_snare:
                nums.append((i+1,j+1,k+1))
                
    return nums
 
    
    
def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

    
def vat_solutions(list_of_compartment_compositions,list_of_vesicle_compositions,vesicle_fusions,nums):
    
    comp_list=list(list_of_compartment_compositions.keys())
    vesicle_all_cov={}
    comp_fuse=[]
    comp_no_fuse=[]
    for z in list(list_of_vesicle_compositions.keys()):  #listofvesicles

      
       

        comp=vesicle_fusions[z]
        for j in comp:
            v_snare=list_of_vesicle_compositions[z]
            v_snare_act=list_of_vesicle_compositions[z]
            t_snare_comp=list_of_compartment_compositions[j]
            v_a_t=[]

            for a in v_snare:
                for b in v_snare_act:
                    for c in t_snare_comp:
                        if (a,b,c)==(1,1,1):
                            v_a_t.append(1)
                        else:
                            v_a_t.append(0)

            comp_fuse.append(v_a_t)


        #comp_fuse=np.array(comp_fuse)


       
        other_comps=diff(comp_list,comp)  #checking against self fusions too
       

        for j in other_comps:
            v_snare=list_of_vesicle_compositions[z]
            v_snare_act=list_of_vesicle_compositions[z]
            t_snare_comp=list_of_compartment_compositions[j]
            v_a_t=[]

            for a in v_snare:
                for b in v_snare_act:
                    for c in t_snare_comp:
                        if (a,b,c)==(1,1,1):
                            v_a_t.append(1)
                        else:
                            v_a_t.append(0)

            comp_no_fuse.append(v_a_t)

        #comp_no_fuse=np.array(comp_no_fuse)

        #print(comp_no_fuse)
    
    comp_fuse=np.array(comp_fuse)
    comp_no_fuse=np.array(comp_no_fuse)
    
    

    col_list_numbers=[]
  
    for i in range(comp_fuse.shape[1]):
            fuse_col=np.count_nonzero(comp_fuse[:,i]==1)
           

            if fuse_col>0:
                if comp_no_fuse.shape[0]>0:
                    fuse_non_col=np.count_nonzero(comp_no_fuse[:,i]==1)
                    if fuse_non_col==0:
                        col_list_numbers.append(i)                             
                else:
                    col_list_numbers.append(i)
 
    cargo_combs=[]
    for i in col_list_numbers:                             #just column numbers not cargo numbers
        cargo_combs.append(nums[i])
  
    flag=0
    for z in list(list_of_vesicle_compositions.keys()):
       
        ves_composition=list_of_vesicle_compositions[z]
        comps=vesicle_fusions[z]
       
        x,y=check_vat_solutions(ves_composition,cargo_combs,comps,list_of_compartment_compositions)
      
        vesicle_all_cov[z]=x[:]
 
        if y=='consistent':
            flag=flag+1
 
    if flag==len(list(list_of_vesicle_compositions.keys())):
        return vesicle_all_cov
    else:
        return {}
  


def check_if_solution_spans_all(col_list_array):
 
    for i in range(col_list_array.shape[0]):

        if np.count_nonzero(col_list_array[i,:]==1)<1:

            return("inconsistent")
  
    return("consistent")


def check_vat_solutions(vesicle_composition,combined_ints,comps,list_of_compartment_compositions):
    #print("comps",comps)
    
    l_o_c_c={}
    keys_list=list(list_of_compartment_compositions.keys())
    
    
    for i in keys_list:
        j=list_of_compartment_compositions[i]
        c=0
        new_value=[]
        if i in comps:
            for k in j:
                c=c+1
                if k==1:
                    new_value.append(c)
            l_o_c_c[i]=new_value[:]
       
   
    vesicle_comp=[]
    c=0
    for i in vesicle_composition:
        c=c+1
        if i==1:
            vesicle_comp.append(c)
  
    comps_covered=[]    
    z_=[]
    #fusions=[]
    
    #non_fusions=[]
    for i in combined_ints:
       
        v_snare,v_snare_a=i[0],i[1]
        t_snare=i[2]
        
        if v_snare in vesicle_comp and v_snare_a in vesicle_comp:
            
            
            d_= list(l_o_c_c.values())
            flag=0
            for p in d_:
                if t_snare in p:
                    flag=1
            if flag==1:
                z_.append(i)
                
            cc=[k for k,v in l_o_c_c.items() if t_snare in v]
           
            comps_covered=comps_covered+cc
    
  
    #checking if the solutions for the given vesicle spans all compartments that it fuses to
    comps.sort()
    comps_covered=list(set(comps_covered))
    comps_covered.sort()
    #print(comps)
    #print(comps_covered)
    if comps_covered==comps:
        return z_,'consistent'
    else:
        z_=[]
        return z_,'inconsistent'
        
########################################################################################################################################################           


#v=0       
#for graph_ in list_of_graphs:
    
def get_graph_solution(graph_):
    #v=v+1
    #print(1)
    
    no_of_coats=3

    graph_vats={} 
    graph_edges=[] 
    graph_comp_and_ves_compositions={}
    
    
    p=0 #consistency
    edge_list=graph_label(graph_)
    
    edge_list.sort()
    #print(edge_list)
    coat_labeled_compositions={}
    coat_labeled_covers={}
    compositions={}

    graph_dictionary_comp_compositions={}
    possible,ER_labels=test_graph_and_possible_ER(edge_list,no_of_coats)
    
    

    compartments=list(set([item for t in edge_list for item in t]))
    list_of_all_cargo=list_of_cargos(no_of_coats)
    compartments.sort()

    if possible==1:   #checking if there are roots other than ER, if there are none - then continue

        #Generate all possible coat_labels for the given graph
        coat_labels_=coat_labels(no_of_coats,edge_list)
        
        cl=[]
        for i in coat_labels_:
            if len(set(i))==no_of_coats:
                cl.append(i)

        coat_ER_labels=list(itertools.product(ER_labels, cl))
       
        for c_label in coat_ER_labels:

            
            chosen_coat_ER_label=c_label

            ER=chosen_coat_ER_label[0]
            
            chosen_coat_label=chosen_coat_ER_label[1]
           
            #possible cargo on each edge

            locs=list_of_cargo_sets(edge_list,chosen_coat_label,no_of_coats)
          

            #initialise cargo compositions for each compartment

            cargos_0=[0] * (2**(no_of_coats))
            cargos_1=[1] * (2**(no_of_coats))


            list_of_compartment_compositions={}
            for i in compartments:
                list_of_compartment_compositions[i]=cargos_0[:]

            list_of_compartment_compositions[ER]=cargos_1[:]

            #initialise vesicle compositions 
            
            list_of_vesicle_compositions={}
            c=0
            for i in edge_list:   #for the vesicle at each edge
                coat=chosen_coat_label[c]
                source=i[0]
                list_of_vesicle_compositions[(coat,source)]=cargos_0[:]
                c=c+1


            #get compartment and vesicle compositions

            for i in list_of_all_cargo:
                

                startnodes,endnodes,all_but_end_nodes,sub_edges=condensed_cargo_subgraph_new(i,edge_list,locs,ER)
               
                if ER in startnodes:

                    cargo_number=int(i[1:])-1

                    for j in all_but_end_nodes:
                        #j=compartment_no
                        comp_cargo=list_of_compartment_compositions[j]
                        comp_cargo[cargo_number]=0
                        list_of_compartment_compositions[j]=comp_cargo[:]

                    for j in endnodes:

                        comp_cargo=list_of_compartment_compositions[j]
                        comp_cargo[cargo_number]=1
                        list_of_compartment_compositions[j]=comp_cargo[:]
                  
                    vesicle_edges,edge_numbers=find_edges_of_strongly_connected_nodes(i,locs,edge_list,endnodes)
                   
                    if len(vesicle_edges)>0:
                        G = nx.DiGraph(vesicle_edges)
                        if nx.is_strongly_connected(G)==True:
                           
                            vesicles=cargo_vesicle_new(i,edge_list,edge_numbers,locs,chosen_coat_label)
                            #print(vesicles)

                            for j in vesicles:

                                ves_cargo=list_of_vesicle_compositions[j]
                                ves_cargo[cargo_number]=1
                                list_of_vesicle_compositions[j]=ves_cargo[:]


            present_compositions=list(list_of_compartment_compositions.values())

            
            c_labeled=(c_label[0],tuple(c_label[1]))
            graph_dictionary_comp_compositions[c_labeled]=present_compositions[:]
            coat_labeled_compositions[c_labeled]=present_compositions[:]
            compositions[c_labeled]=list_of_compartment_compositions,list_of_vesicle_compositions
                    
                    



        graph_comp_and_ves_compositions[tuple(edge_list)]=compositions
        graph_edges.append(edge_list)
        
        
        
        return graph_comp_and_ves_compositions

############################################################################################################################

# directory = './'
output_directory = '/home/thattai/kritikak/Param_Brahma_IISERP/'
output_filename = 'All_4c12e.txt'
output_path = os.path.join(output_directory, output_filename)
graph = sys.argv[1]
graph=ast.literal_eval(graph)
result_graphs=get_graph_solution(graph)

'''if os.path.exists(output_path):
    data = []
    with open(output_path, 'rb') as f:
        dat = pickle.load(f)
        data.append(dat)
    data.append(result_graphs)
    with open(output_path, 'wb') as f:
        pickle.dump(data, f) 
else:
    with open(output_path, 'wb') as f:
        pickle.dump(result_graphs, f)'''


with open(output_path,'a+') as f:
#    graph = sys.argv[1]
#    graph=ast.literal_eval(graph)
#    result_graphs=get_graph_solution(graph)

    f.writelines(str(result_graphs)+'\n')
