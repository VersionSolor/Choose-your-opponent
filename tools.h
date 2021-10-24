#pragma once
#include <Imagine/Graphics.h>
#include "Imagine/LinAlg.h"
#include <Imagine/Graphics.h>
#include <forward_list>
#include "vectortree.h"



VectorTree* empty_Q_P_N(unsigned int N,int c_player);

double p_S(const std::vector<bool>& S,const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::Matrix<double>& probability_matrix);

double qSaj(int j, std::vector<double>& qS, std::vector<int>& X1, std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix);

void opponent_choice_optimization_algorithm(std::vector<int>& X1,std::vector<int>& X2,std::forward_list<double>& ranking,unsigned int n,VectorTree* QOmega, const Imagine::Matrix<double>& probability_matrix);

void setMatrixVictory(Imagine::Matrix<double> &M);

void display(const Imagine::Matrix<double> &M);
