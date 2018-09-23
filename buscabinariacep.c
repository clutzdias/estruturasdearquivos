#include <stdio.h>

typedef struct _Endereco Endereco;

struct _Endereco{
	char logradouro[72];
	char bairro[72];
	char cidade[72];
	char uf[72];
	char sigla[2];
	char cep[8];
	char lixo[2];
};

void buscaCep (long fim, FILE *f, char* cep){

	//o meio tem que ser calculado dentro do loop, pois ele muda a cada iteração da busca
	//o fseek do loop determina a posicao absoluta do meio
	
	int qt;
	int i = 0;
	long inicio = 0;
	long meio;
	Endereco e;
	while (inicio <= fim){
		i++;
		meio = (inicio + fim)/2;
		fseek(f, meio*sizeof(Endereco), SEEK_SET);
		qt = fread(&e, sizeof(Endereco), 1, f);
		if(strncmp(cep, e.cep, 8) == 0){ // compara com 0, pois está comparando strings. Se tiverem o mesmo tamanho, a diferença será 0.
			printf("%.72s\n%.72s\n%.72s\n%.72s\n%.2s\n%.8s\n",e.logradouro,e.bairro,e.cidade,e.uf,e.sigla,e.cep);
			break;
		}else{
			if (strncmp(cep,e.cep,8) < 0){
				fim = meio - 1;
			}else{
				inicio = meio + 1;
			}
		}
	}
	printf("Quantidade de passagens: %d", i);

}
	
int main(int argc, char**argv)
{
	FILE *f;
	Endereco e;
	long posicao, ultimo;

	
	//caso os parâmetros estejam incorretos, informa como o usuário deve proceder
	if(argc != 2)
	{
		fprintf(stderr, "USO: %s [CEP]", argv[0]);
		return 1;
	}
	
	//abre o arquivo e determina o tamanho total do mesmo em bytes
	f = fopen("cep_ordenado.dat","r");
	fseek(f,0,SEEK_END);
	posicao = ftell(f);
	rewind(f);

	//Determina o fim do arquivo
	ultimo = (posicao/sizeof(Endereco)) - 1;

	buscaCep(ultimo, f, argv[1]);

	fclose(f);

	return 0;

}







