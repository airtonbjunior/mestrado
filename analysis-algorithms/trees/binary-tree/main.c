#include <stdio.h>
#include <stdlib.h>

/* Node of the tree */
typedef struct reg {
	int key;
	struct reg *left;
	struct reg *right;
	
} node;


typedef node *tree;


/*	Return the size of the tree 
	The "+1" indicates the root node
*/
int size(tree t) {
	if (t == NULL)
		return 0;
	else 
		return size(t->left) + 1 + size(t->right);
}

/* 	Return the height of the tree 
	t can be any node of the tree, not only the main root
*/
int height(tree t) {
	if (t == NULL) return -1;
	else{
		int lh = height(t->left);
		int rh = height(r->right);
		if(lh < rh) 
			return rh + 1 
		else 
			return lh + 1;
	}
}

int main(int argc, char *argv[]) {
	return 0;
}
