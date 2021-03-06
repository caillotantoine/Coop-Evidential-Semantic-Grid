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


#define VALMAX              -1
#define MAXBETP             0
#define MAXBEL              1
#define MAXPL               2
#define MAXBBA              3
#define PEST                4
#define WPEST               5

#define VEHICLE_ELEM_ID     0b001
#define PEDESTRIAN_ELEM_ID  0b010
#define TERRAIN_ELEM_ID     0b100

#ifdef _MSC_VER
    #include <intrin.h>
    #define COUNT_BITS      __popcnt
#else
    #define COUNT_BITS      __builtin_popcount
#endif

void decision_CPP(float *evid_map_in, unsigned char *sem_map, int gridsize, int nFE, int method);
float betP(float *elems, unsigned char set, int nFE);
float bel(float *elems, unsigned char set, int nFE);
float pl(float *elems, unsigned char set, int nFE);
float Pest(float *elems, unsigned char set, int nFE);
float wPest(float *elems, unsigned char set, int nFE);

extern "C" {
    void decision(float *evid_map_in, unsigned char *sem_map, int gridsize, int nFE, int method)
        {decision_CPP(evid_map_in, sem_map, gridsize, nFE, method);}
}

int main(int argc, char **argv)
{
    // float elems[2][2][8] = {{{0.0, 0.6, 0.05, 0.1, 0.05, 0.1, 0.0, 0.1}, {0.0, 0.05, 0.6, 0.1, 0.05, 0.1, 0.0, 0.1}}, {{0.0, 0.05, 0.05, 0.1, 0.6, 0.1, 0.0, 0.1}, {0.0, 0.1, 0.1, 0.2, 0.1, 0.2, 0.15, 0.15}}};
    // int nFE = 8;
    // unsigned char out[2][2] = {0};
    // printf("betP(V) = %f\n", betP((float *) elems + 2 * nFE , VEHICLE_ELEM_ID, nFE));
    // decision_CPP((float *) elems, (unsigned char *) out, 2, nFE, 0);
    //printf("%d\n", COUNT_BITS(3));
    // float res[8] = {0.0000,  0.1346,  0.6250,  0.0962,  0.0865,  0.0577,  0.0000,  0.0000 };
    float res[8] = {0.1680,  0.1120,  0.5200,  0.0800,  0.0720,  0.0480,  0.0000,  0.0000};
    printf("bel: %.4f\n", bel(res, 0x01, 8));
    printf("pl: %.4f\n", pl(res, 0x01, 8));
    printf("Pest: %.4f\n", Pest(res, 0x01, 8));
    printf("wPest: %.4f\n", wPest(res, 0x01, 8));

    printf("\n\n");

    printf("bel: %.4f\n", bel(res, 0x02, 8));
    printf("pl: %.4f\n", pl(res, 0x02, 8));
    printf("Pest: %.4f\n", Pest(res, 0x02, 8));
    printf("wPest: %.4f\n", wPest(res, 0x02, 8));

    return 0;
}

float betP(float *elems, unsigned char set, int nFE)
{
    unsigned char B = 0;
    float sum = 0;
    for( B = 1; B < nFE; B++) // B = 1 -> avoiding empty set
        sum += elems[B] * (((float) COUNT_BITS(set & B)) / ((float) COUNT_BITS(B))); // BetP formula. Cardinality is found by counting the numbers of bits in the byte.
    return sum;
}

float bel(float *elems, unsigned char set, int nFE)
{
    float sum = 0;
    unsigned char B = 0;
    for(B = 1; B < nFE; B++)
        if((B|set) == set)
            sum += elems[B];
    return sum;
}

float pl(float *elems, unsigned char set, int nFE)
{
    float sum = 0;
    unsigned char B = 0;
    for(B = 1; B < nFE; B++)
        if((B&set) != 0x00)
            sum += elems[B];
    return sum;
}

float Pest(float *elems, unsigned char set, int nFE)
{
    float vbel = 0.0;
    float vpl = 0.0;
    vbel = bel(elems, set, nFE);
    vpl = pl(elems, set, nFE);
    return ((vpl - vbel) / 2.0) + vbel;
}

float wPest(float *elems, unsigned char set, int nFE)
{
    float vbel = 0.0;
    float vpl = 0.0;
    vbel = bel(elems, set, nFE);
    vpl = pl(elems, set, nFE);
    return (((vpl - vbel) / 2.0) + vbel) * (1-(vpl - vbel));
}

void decision_CPP(float *evid_map_in, unsigned char *sem_map, int gridsize, int nFE, int method)
{
    int i = 0, j = 0, max_elem_id = 0;
    float val = 0;
    float maxprev = -1.0;
    const unsigned char LUT[3] = {VEHICLE_MASK, PEDESTRIAN_MASK, TERRAIN_MASK};

    // printf("Methode : %d\n", method);

    // printf("1 : %x\n", LUT[0]);
    // printf("2 : %x\n", LUT[1]);
    // printf("3 : %x\n", LUT[2]);
    for(i = 0; i<gridsize*gridsize; i++)
    {
        maxprev = -1;
        sem_map[i] = 0x01;
        // printf("ID %d: \t", i);
        for(j = 0; j<3; j++)
        {
            switch(method)
            {
                case -1:
                    val = evid_map_in[i*3 + j];
                    break;
                    
                case MAXBETP:
                    val = betP((evid_map_in + i * nFE), VEHICLE_ELEM_ID<<j, nFE);
                    break;

                case MAXBEL:
                    val = bel((evid_map_in + i * nFE), VEHICLE_ELEM_ID<<j, nFE);
                    break;

                case MAXPL:
                    val = pl((evid_map_in + i * nFE), VEHICLE_ELEM_ID<<j, nFE);
                    break;

                case MAXBBA:
                    val = evid_map_in[(i * nFE) + (VEHICLE_ELEM_ID<<j)];
                    break;

                case PEST:
                    val = Pest((evid_map_in + i * nFE), VEHICLE_ELEM_ID<<j, nFE);
                    break;

                case WPEST:
                    val = wPest((evid_map_in + i * nFE), VEHICLE_ELEM_ID<<j, nFE);
                    break;

                default:
                    val = 0;
                    break;
            }
                        // printf("ELEM %x: %.3f \t", j, val);
            if(val >= maxprev)
            {
                maxprev = val;
                max_elem_id = j;
            }
        }
        sem_map[i] = LUT[max_elem_id];
        // printf("set %0x : %x\n", max_elem_id, LUT[max_elem_id]);
        // printf("max for %x: %.3f\n", max_elem_id, maxprev);
    }
}

