#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>

#define VEHICLE_MASK        0b01000000
#define PEDESTRIAN_MASK     0b10000000
#define TERRAIN_MASK        0b00000010

#define DEMPSTER            0x00
#define CONJUNCTIVE         0x01
#define DISJUNCTIVE         0x02

#define CUDA_BLOCKWIDTH     (256)
#define N_CLASSES           8

// CPP function to be available on library front end
// void bonjour_cpp();
void mean_merger_cpp(unsigned char *masks, int gridsize, int n_agents, float *out, float *FE, const int nFE);
void DST_merger_CPP(float *evid_maps_in, float *inout, int gridsize, int nFE, int n_agents, unsigned char method);

// Merging functions, either for CUDA and CPP
void conjunctive(float *inout_cell, float *cell, int n_elem, bool dempster);
void disjunctive(float *inout_cell, float *cell, int n_elem);
float Konflict(float *inout_cell, float *cell, int n_elem);


// Interface of the SO library
extern "C" {
    void mean_merger(unsigned char *masks, int gridsize, int n_agents, float *out, float *FE, const int nFE)
        {mean_merger_cpp(masks, gridsize, n_agents, out, FE, nFE);}
    void DST_merger(float *evid_maps_in, float *inout, int gridsize, int nFE, int n_agents, unsigned char method)
        {DST_merger_CPP(evid_maps_in, inout, gridsize, nFE, n_agents, method);}
}

//////////////////////////
//                      //
//     CUDA kernels     //
//                      //
//////////////////////////

// TODO : Doesn't work. Seem to only process the first agent, thus, no merging done. 
//   NOTE : I certainly messed up with memory management in somewhere.

void conjunctive_kernel(float *evid_maps_in, float *inout, const int gridsize, const int nFE, const int n_agents)
{
    const long i = 0;
    int j = 0;
    if(i < (gridsize * gridsize))
    {
        for(j = 0; j < n_agents; j++)
        {
            conjunctive((inout + i*nFE), (evid_maps_in + i*nFE*n_agents + j*nFE), nFE, false);
        }
    }
}

void dempster_kernel(float *evid_maps_in, float *inout, const int gridsize, const int nFE, const int n_agents)
{
    const long i = 0;
    int j = 0;
    if(i < (gridsize * gridsize))
    {
        for(j = 0; j < n_agents; j++)
            conjunctive((inout + i*nFE), (evid_maps_in + i*nFE*n_agents + j*nFE), nFE, true);
    }
}

void disjunctive_kernel(float *evid_maps_in, float *inout, const int gridsize, const int nFE, const int n_agents)
{
    int i = 0;
    int j = 0;

    if(i < (gridsize * gridsize))
    {
        for(j = 0; j < n_agents; j++)
            disjunctive((inout + i*nFE), (evid_maps_in + i*nFE*n_agents + j*nFE), nFE);
    }
}


///////////////////////////
//                       //
//   Merging functions   //
//                       //
///////////////////////////

void conjunctive(float *inout_cell, float *cell, int n_elem, bool dempster)
{
    int A = 0, B = 0, C = 0, i = 0;
    float buf[N_CLASSES] = {0};
    float res;
    float K = 0.0;
    if(dempster)
        K = 1.0 / (1.0 - Konflict(inout_cell, cell, n_elem));
    for (A = 1; A<n_elem; A++) // A starts from 1 since there must be A != Ø
    {
        for(B=0; B<n_elem; B++)
        {
            for(C=0; C<n_elem; C++)
            {
                if((B&C) == A)
                {
                    res = (float) *(inout_cell + B) * (float) *(cell + C);
                    // printf("A %f, %f, %f\n",*(inout_cell + B), *(cell + C), res);
                    buf[A] += res;
                }
            }
        }
        if(dempster)
            buf[A] *= K;
    }
    for(i = 0; i<N_CLASSES; i++)
        inout_cell[i] = buf[i];
    // memcpy(inout_cell, buf, sizeof(float)*n_elem);
}

void disjunctive(float *inout_cell, float *cell, int n_elem)
{
    int A = 0, B = 0, C = 0, i=0;
    float buf[N_CLASSES] = {0};
    float res;
    for (A = 0; A<n_elem; A++)
    {
        for(B=0; B<n_elem; B++)
        {
            for(C=0; C<n_elem; C++)
            {
                if((B|C) == A)
                {
                    res = (float) *(inout_cell + B) * (float) *(cell + C);
                    // printf("A %f, %f, %f\n",*(inout_cell + B), *(cell + C), res);
                    buf[A] += res;
                }
            }
        }
    }
    for(i = 0; i<N_CLASSES; i++)
        inout_cell[i] = buf[i];
    // memcpy(inout_cell, buf, sizeof(float)*n_elem);
}

float Konflict(float *inout_cell, float *cell, int n_elem)
{
    int B = 0, C = 0;
    float res = 0;
    for(B=0; B<n_elem; B++)
    {
        for(C=0; C<n_elem; C++)
        {
            if((B|C) == 0)
            {
                res += (float) *(inout_cell + B) * (float) *(cell + C);
            }
        }
    }
    return res;
}


/////////////////////////
//                     //
//     Entry point     //
//                     //
/////////////////////////

using namespace std;

int main(int argc, char **argv)
{
    
    // float U[8] = {0.1, 0, 0, 0, 0, 0, 0, 0.9};
    // float T[8] = {0.05, 0, 0, 0, 0.7, 0.05, 0.05, 0.15};

    float U[8] = {0.0, 0, 0, 0, 0, 0, 0, 1.0};
    float T[8] = {0.0, 0, 0, 0, 0.7, 0.05, 0.05, 0.2};

    // float A[4][8] = {U, U, U, U};
    // float B[4][8] = {T, T, T, T};

    float out[8] = {0};
    memcpy(out, U, 8*sizeof(float));

    conjunctive(out, U, 8, true); 
    conjunctive(out, U, 8, true);
    conjunctive(out, U, 8, true);
    conjunctive(out, U, 8, true);
    conjunctive(out, U, 8, true);
    conjunctive(out, U, 8, true);
    conjunctive(out, T, 8, true);
    conjunctive(out, T, 8, true);


    
    return 0;
}

//////////////////////////
//                      //
//       Functions      //
//                      //
//////////////////////////


float get_normFactor(float *FE, const int nFE, int row)
{
    float normFactor = 0.0;
    int i = 0;
    for (i = 1; i<5; i<<=1)
        normFactor += FE[row * nFE + i];
    return 1.0/normFactor;
}

// Merger code for averaging cells

void mean_merger_cpp(unsigned char *masks, int gridsize, int n_agents, float *out, float *FE, const int nFE)
{
    int l = 0, i = 0, c = 0, j = 0;
    int idx = 0;
    float normFactor = 0.0;

    // for(i = 0; i<5; i++)
    // {
    //     for(j = 0; j<nFE; j++)
    //     {
    //         printf("%2.3f \t", FE[i*nFE + j]);
    //     }
    //     printf("\n");
    //     for(j = 0; j<3; j++)
    //         printf("%d - %2.3f \t", 1<<j, FE[i * nFE + (1<<j)]);
    //     printf("\n\n");
    // }

    for(i=0; i<gridsize*gridsize; i++)
    {
        for(l=0; l<n_agents; l++)
        {
            switch(masks[i*n_agents + l])
            {
                case VEHICLE_MASK:
                    #define FEROW 1
                    for(j = 0; j<3; j++)
                        out[(i*3) + j] += FE[FEROW * nFE + (1<<j)] * normFactor;
                    // out[(i*3) + 0] += 1.0;
                    // out[(i*3) + 1] += 0.0;
                    // out[(i*3) + 2] += 0.0;
                    break;

                case PEDESTRIAN_MASK:
                    #define FEROW 2
                    normFactor = get_normFactor(FE, nFE, FEROW);
                    for(j = 0; j<3; j++)
                        out[(i*3) + j] += FE[FEROW * nFE + (1<<j)] * normFactor;
                    // out[(i*3) + 0] += 0.0;
                    // out[(i*3) + 1] += 1.0;
                    // out[(i*3) + 2] += 0.0;
                    break;

                case TERRAIN_MASK:
                    #define FEROW 3
                    normFactor = get_normFactor(FE, nFE, FEROW);
                    for(j = 0; j<3; j++)
                        out[(i*3) + j] += FE[FEROW * nFE + (1<<j)] * normFactor;
                    // out[(i*3) + 0] += 0.0;
                    // out[(i*3) + 1] += 0.0;
                    // out[(i*3) + 2] += 1.0;
                    break;
                
                default:
                    #define FEROW 3
                    for(j = 0; j<3; j++)
                        out[(i*3) + j] += 0.5;
                    // out[(i*3) + 0] += 0.5;
                    // out[(i*3) + 1] += 0.5;
                    // out[(i*3) + 2] += 0.5;
                    break;
            }
        }
    }
    for(i = 0; i<(gridsize*gridsize*3); i++)
        out[i] /= n_agents; ////
}

// Merger function to merge the cells using Dempster Shaffer Theory 

void DST_merger_CPP(float *evid_maps_in, float *inout, int gridsize, int nFE, int n_agents, unsigned char method)
{
    int l = 0, i = 0, j =0;
    for(i=0; i<gridsize*gridsize; i++)
    {
        for(j = 0; j<n_agents; j++)
        {
            //inout[i*nFE /*+ channel index*/] = evid_maps_in[i*nFE*n_agents + j*nFE /*+ channel index*/];
            switch(method)
            {
                case CONJUNCTIVE:
                    conjunctive((inout + i*nFE), (evid_maps_in + i*nFE*n_agents + j*nFE), nFE, false);
                    break;
                
                case DISJUNCTIVE:
                    disjunctive((inout + i*nFE), (evid_maps_in + i*nFE*n_agents + j*nFE), nFE);
                    break;

                case DEMPSTER:
                    conjunctive((inout + i*nFE), (evid_maps_in + i*nFE*n_agents + j*nFE), nFE, true);
                    break;

                default:
                    printf("No fusion method for the following value: %d", method);
                    break;
            }
        }   
    }

}



