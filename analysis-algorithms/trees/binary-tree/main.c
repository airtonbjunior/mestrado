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


int main(int argc, char *argv[]) {
	return 0;
}
