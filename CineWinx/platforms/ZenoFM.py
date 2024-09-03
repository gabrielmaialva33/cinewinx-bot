import json
from typing import Union, Dict, Any, Optional, TypedDict, List

import aiohttp

#
# https://zeno.fm/api/stations/?query=&limit=24&genre=Music&country=Brazil&language=Portuguese+%28Brazil%29&page=1

# [
#     {
#         "url": "https://zeno.fm/radio/melodias-e-momentos/",
#         "name": "Melodias e Momentos",
#         "logo": "https://images.zeno.fm/u7AUniEh6DuhR7kDHtfL56C7u86f62XEr37wRQDSZdg/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zLzcwNzYwNDkxLTU0ZTEtNDAzYS04OThiLTc1NGE2ZWM5Mzg4NS9pbWFnZS8_dXBkYXRlZD0xNzIxODQyNTkxMDAwP3U9NTc1MTEwOQ.webp",
#         "featured": true,
#         "sponsored": true
#     },
#     {
#         "url": "https://zeno.fm/radio/groupe-medialternatif-haiti/",
#         "name": "Groupe Medialternatif - Haiti",
#         "logo": "https://images.zeno.fm/JnYp8CgK3vAjn5hwqQ32WhhaFnMhQshbvf0F6I85pKY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNBb0t5T21na01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURJdVlHLXdRc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjAyNTA0NzAwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": true
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-buteco-sertanejo/",
#         "name": "Radio Buteco Sertanejo",
#         "logo": "https://images.zeno.fm/Y6LMJnlACVswrA4b-ny-lSeUz5ALokFqbYXfNbDxuxE/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnNV96cnBnc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnbDh5UHJ3c01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTQ2OTYwNDUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/amado-batista/",
#         "name": "Rádio Amado Batista",
#         "logo": "https://images.zeno.fm/0lKsmbs8Yg5y3JjImuPPpylH68a-SbACNFB-utm6VB8/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnbmRMWHZBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnMGRiRWdBc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2OTUyMjE5ODIwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/sertaneja-fm/",
#         "name": "SERTANEJA FM",
#         "logo": "https://images.zeno.fm/ilVwr34MrGWVbU4YjYq3ZOMT8qoaj-l3muKSPBTdqus/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnajZQMHdBa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnOThEcmtRc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTU4NDUzNTYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/sertanejo-fm-alta-qualidade/",
#         "name": "Sertanejo FM - Alta qualidade",
#         "logo": "https://images.zeno.fm/EGgdxtOurk-R9Qkmj5hlXole0ERWc1KH5li_a33Gps8/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURRcGRxWW93c01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUR3d2V5UjFna01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MDQxNDkwNzkwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/tempofm1039/",
#         "name": "Tempo Fm 103.9",
#         "logo": "https://images.zeno.fm/UtCLsFQD1EhJcbq7uzIztztzHJ5D2pgTibeXfuZc530/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURRLXJPbjVRb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURReHJpaW1Rb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjA4NTY0NDUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/ForroDasAntigas/",
#         "name": "Rádio Forró  Das Antigas",
#         "logo": "https://images.zeno.fm/cUGI-cqliVjtqQs8IFkQGo2ZbPKxag8gz4BrtrSr5YQ/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURndDRiVHBBa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURndDhYeHp3b01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjExMjMwMTEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/bobmarley/",
#         "name": "MARLEY",
#         "logo": "https://images.zeno.fm/vZJvNo9i5XhWUZLgucg7-tX_vAXBsokskNIxPNCgfAk/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnek91SHlBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURJeEl5cTNBZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MDg1NjAxNjEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-carro-de-boi/",
#         "name": "Radio Carro de Boi",
#         "logo": "https://images.zeno.fm/skABB3iIk5xBwe8KnRU3bUAQeYokzm_oV7VGt3NwGXE/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUN3aHJuZi1Rc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUN3N3JTT3lna01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODcyNzUzOTMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/flashdance90/",
#         "name": "FLASH  DANCE  90",
#         "logo": "https://images.zeno.fm/V6si6afg7KTH4Rdp7IVAlMvXm0C8TpFiuXcbFAZon6k/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnek91SHlBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRZ09PcHlRZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MDg1NjAxMDMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/mega-radio-pagode/",
#         "name": "Mega Radio Pagode",
#         "logo": "https://images.zeno.fm/Zimf0DaD2qEUpqDvaBljZqNQ67-wAdHqPcb9e7lZCVY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNndTd1Z25nZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNncDRIVXlnc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODYwODYwOTMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/brega-show-2/",
#         "name": "Rádio Brega Fm",
#         "logo": "https://images.zeno.fm/ubD9ph34AmLqOVqhWI7W1DdIDo1MIs147c8zDMUYSj0/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnbmRMWHZBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURndl91bWdRa01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODE3ODE3MzYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/mega-radio-love/",
#         "name": "Mega Radio Love",
#         "logo": "https://images.zeno.fm/ERsxNDhUoOb6_dNxMkn7mOQCQRxkknXXID5Mr8TmJrg/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNndTd1Z25nZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnNUo3T2lBc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODY3OTgyMjEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/a-voz-do-gueto/",
#         "name": "Radio Rap a Voz do Gueto",
#         "logo": "https://images.zeno.fm/8MvG6qEwXCha5MY48OVUP6yAVfGglUSdMAK6mpZH6FQ/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnLXNESzdBa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnLXNENzdnZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjExNTc3OTEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/lancamentos-sofrenejo/",
#         "name": "Lançamentos - Sertanejo e Sofrência",
#         "logo": "https://images.zeno.fm/YkAoyTxbKFa6pcnwqF-xTLWkDR8_6ExNMXTuMklYjXA/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnb3RPY3d3Z01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRNGNqNnJRZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE2NTQxMTIwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-musica-das-antigas/",
#         "name": "Radio Musica das Antigas",
#         "logo": "https://images.zeno.fm/gUStAZywORyUwzzKVmIQIcG2fYHREI217aId5iD-VHo/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNRNl9HVHZBZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRNi1lN2xRc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjEzNjA3NDYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/funk-brasil/",
#         "name": "FUNK BRASIL",
#         "logo": "https://images.zeno.fm/_cZGtqiu2_s9ah3wLL-j5EkgoPLC4cB2iM5UADFDWZw/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnNHZYYXV3Z01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnN3Z6WXJRZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE1MDc4NDUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/jolimpb/",
#         "name": "Joli MPB",
#         "logo": "https://images.zeno.fm/MTY2yml4yf79pCq29yNDDUJeGOGUJyTOQ7FVH8ycxdY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnNnNiSTFRc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnbHZ5ZGlBZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE3MjQzNjIwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-rock-fm/",
#         "name": "Radio Rock FM",
#         "logo": "https://images.zeno.fm/XfZDKfLMvSlEGL76kymLWvlolbtVaYemvSFcXfVZXPY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURBdGZhcy1nb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNBZ0lEeWlBb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NzA4MDA0NjQwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/rapsul/",
#         "name": "RAP SUL",
#         "logo": "https://images.zeno.fm/WbtTc3FJkwIhP62v07SqVXJ6L57Gi_rPCjt2dpgWWzc/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnLTd1VnRBc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnaF9ISnd3a01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE3MTkwNjMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/conexaojamaica/",
#         "name": "CONEXÃO JAMAICA",
#         "logo": "https://images.zeno.fm/1Cg6DNE0gK-qakOZ8yudhKkYL-BNW0fVa8_EwmH7lZs/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURndnNydzJRa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRMVlQNmpRb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTEzNDEyNjYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/forro-das-antigas/",
#         "name": "Radio forró das antigas",
#         "logo": "https://images.zeno.fm/JZlu5amD0lgOLpUyaVGSF0uC4mCnu8AqSvIkvfalV00/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURBd2NxVDN3c01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnOWRIRzV3b01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODUwMzUxMjYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/mega-radio-sertanejo/",
#         "name": "Mega Radio Sertanejo",
#         "logo": "https://images.zeno.fm/mQtflodMwj2cyBFiTVTS3XP-3F7DXTX4FvYGuF6Qud4/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNndTd1Z25nZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnaE4tOWtBb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTk4NDYxOTUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     }
# ]


class ListStation(TypedDict):
    url: str
    name: str
    logo: str
    featured: bool
    sponsored: bool


class ZenoFMAPI:
    def __init__(self):
        self.url: str = "https://zeno.fm/api"
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url: str = "https://zeno.fm"
        self.session_headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Content-Type": "application/json",
        }

        self.timeout: int = 60

    async def request(
        self, endpoint: str, method: str, data: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], str, None]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method, self.url + endpoint, headers=self.session_headers, json=data
                ) as response:
                    content_type: str = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        return await response.json()
                    else:
                        text: str = await response.text()
                        try:
                            return json.loads(text)
                        except json.JSONDecodeError:
                            return text
            except Exception as e:
                print(e)
                return None

    async def get_stations(
        self,
        query: str = "",
        page: int = 1,
        limit: int = 24,
        genre: str = "Music",
        country: str = "Brazil",
        language: str = "Portuguese (Brazil)",
    ) -> Optional[List[ListStation]]:
        response: Optional[List[ListStation]] = await self.request(
            f"/stations/?query={query}&limit={limit}&genre={genre}&country={country}&language={language}&page={page}",
            "GET",
        )

        return response
