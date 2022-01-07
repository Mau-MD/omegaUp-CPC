#include <bits/stdc++.h>

using namespace std;

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int n, m;
    cin >> n >> m;
    char mat[n][m];

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            cin >> mat[i][j];
        }
    }

    int p;
    cin >> p;
    vector<string> palabras;
    for (int i = 0; i < p; i++)
    {
        string a;
        cin >> a;
        palabras.push_back(a);
    }

    int dx[] = {1, 1, 0, -1, -1, -1, 0, 1};
    int dy[] = {0, 1, 1, 1, 0, -1, -1, -1};

    for (int q = 0; q < palabras.size(); q++)
    {
        int ans = 0 ;
        string pActual = palabras[q]; // El que estoy buscando
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {

                if (mat[i][j] == pActual[0]) // Me aseguro que sea igual a la primera letra que estoy buscando
                {
                    for (int k = 0; k < 8; k++) // Depende de la k, la direcion
                    {
                        int x = j + dx[k];
                        int y = i + dy[k];
                        int indice = 1;

                        if (x >= 0 && y >= 0 && x < m && y < n)
                        {
                            if (mat[y][x] == pActual[indice]) // Continuo
                            {
                                bool flag = true;
                                indice++;
                                switch (k)
                                {
                                    case 0: // Derecha aumentar x
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            x++;
                                            if (mat[y][x] != pActual[indice] || x >= m)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                    case 1: //  Diagonal abajo derecha
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            x++, y++;
                                            if (mat[y][x] != pActual[indice] || x >= m || y >= n)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                    case 2: //Abajo
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            y++;
                                            if (mat[y][x] != pActual[indice] || y >= n)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                    case 3: // Diagonal Abajo izquierda
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            x--,y++;
                                            if (mat[y][x] != pActual[indice] || x < 0 || y >= n)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                    case 4: // Atras
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            x--;
                                            if (mat[y][x] != pActual[indice] || x < 0)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                    case 5: //  Diagonal arriba izquierda
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            x--, y--;
                                            if (mat[y][x] != pActual[indice] || x < 0 || y < 0)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                    case 6: //Arriba
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            y--;
                                            if (mat[y][x] != pActual[indice] || y < 0)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                    case 7: // diagonal arriba derecha
                                    {
                                        for (;indice < pActual.size();indice++)
                                        {
                                            x++, y--;
                                            if (mat[y][x] != pActual[indice] || x >= m || y < 0)
                                            {
                                                flag = false;
                                                break;
                                            }
                                        }
                                        if (flag) // Encontre una palabra
                                        {
                                            ans++;
                                        }
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        cout<<ans<<" ";
    }


        return 0;
    }