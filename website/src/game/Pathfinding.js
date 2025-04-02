// src/game/Pathfinding.js
export default class Pathfinding {
    constructor(tileMap) {
      this.tileMap = tileMap;
    }
  
    // Méthode principale pour trouver un chemin entre deux points
    findPath(startX, startY, endX, endY) {
      // Créer les noeuds de départ et d'arrivée
      const startNode = {
        x: startX,
        y: startY,
        g: 0,
        h: this.heuristic(startX, startY, endX, endY),
        f: 0,
        parent: null
      };
      startNode.f = startNode.g + startNode.h;
  
      // Listes ouverte et fermée pour l'algorithme A*
      const openList = [startNode];
      const closedList = [];
      
      // Tant qu'il y a des noeuds à explorer
      while (openList.length > 0) {
        // Trier la liste ouverte par score f (plus petit d'abord)
        openList.sort((a, b) => a.f - b.f);
        
        // Prendre le noeud avec le meilleur score
        const currentNode = openList.shift();
        
        // Vérifier si on est arrivé à destination
        if (currentNode.x === endX && currentNode.y === endY) {
          // Reconstruire le chemin
          return this.reconstructPath(currentNode);
        }
        
        // Ajouter le noeud courant à la liste fermée
        closedList.push(currentNode);
        
        // Explorer les voisins (sans diagonales pour un déplacement de type grille)
        const neighbors = this.getNeighbors(currentNode.x, currentNode.y);
        
        for (const neighbor of neighbors) {
          // Vérifier si le voisin est déjà dans la liste fermée
          if (closedList.some(node => node.x === neighbor.x && node.y === neighbor.y)) {
            continue;
          }
          
          // Calculer le nouveau coût g (distance du départ)
          const newG = currentNode.g + 1; // Coût de 1 pour chaque pas
          
          // Vérifier si le voisin est déjà dans la liste ouverte
          const existingNode = openList.find(node => node.x === neighbor.x && node.y === neighbor.y);
          
          if (!existingNode) {
            // Nouveau noeud, l'ajouter à la liste ouverte
            const newNode = {
              x: neighbor.x,
              y: neighbor.y,
              g: newG,
              h: this.heuristic(neighbor.x, neighbor.y, endX, endY),
              parent: currentNode
            };
            newNode.f = newNode.g + newNode.h;
            openList.push(newNode);
          } else if (newG < existingNode.g) {
            // Meilleur chemin trouvé, mettre à jour le noeud existant
            existingNode.g = newG;
            existingNode.f = existingNode.g + existingNode.h;
            existingNode.parent = currentNode;
          }
        }
      }
      
      // Aucun chemin trouvé
      return [];
    }
    
    // Heuristique : distance de Manhattan (pour déplacements en grille sans diagonales)
    heuristic(x1, y1, x2, y2) {
      return Math.abs(x1 - x2) + Math.abs(y1 - y2);
    }
    
    // Récupérer les voisins valides d'une position
    getNeighbors(x, y) {
      const neighbors = [];
      const directions = [
        {dx: 0, dy: -1}, // haut
        {dx: 1, dy: 0},  // droite
        {dx: 0, dy: 1},  // bas
        {dx: -1, dy: 0}  // gauche
      ];
      
      for (const dir of directions) {
        const newX = x + dir.dx;
        const newY = y + dir.dy;
        
        // Vérifier si la position est valide
        if (this.tileMap.isValidPosition(newX, newY)) {
          neighbors.push({x: newX, y: newY});
        }
      }
      
      return neighbors;
    }
    
    // Reconstruire le chemin en remontant les parents
    reconstructPath(endNode) {
      const path = [];
      let currentNode = endNode;
      
      while (currentNode) {
        path.unshift({x: currentNode.x, y: currentNode.y});
        currentNode = currentNode.parent;
      }
      
      return path;
    }
  }