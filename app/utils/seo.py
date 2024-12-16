from typing import Dict, List, Optional

class SEOHelper:
    @staticmethod
    def get_meta_tags(
        title: str,
        description: str,
        keywords: List[str],
        og_type: str = "website",
        og_image: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate meta tags for SEO optimization."""
        meta_tags = {
            "title": title,
            "description": description,
            "keywords": ", ".join(keywords),
            "og:title": title,
            "og:description": description,
            "og:type": og_type,
        }
        
        if og_image:
            meta_tags["og:image"] = og_image
            
        return meta_tags

    @staticmethod
    def get_page_metadata() -> Dict[str, Dict]:
        """Get metadata for all pages."""
        return {
            "home": {
                "title": "Spranki - Interactive Music and Gaming Experience",
                "description": "Discover Spranki - An immersive musical gaming experience. Play the Spranki game, explore coloring activities, and enjoy interactive music features.",
                "keywords": ["spranki", "sprankį", "sprankiy", "sprankis", "spranki game", "spranki coloring", "music game", "interactive music", "educational game"],
                "og_image": "/static/images/spranki-home.jpg"
            },
            "game": {
                "title": "Play Spranki Game - Interactive Musical Adventure",
                "description": "Play the exciting Spranki game! Combine music and gaming in this unique interactive experience. Perfect for music lovers and gamers alike.",
                "keywords": ["spranki game", "sprankiy game", "sprankis game", "music game", "interactive game", "educational music game"],
                "og_image": "/static/images/spranki-game.jpg"
            },
            "coloring": {
                "title": "Spranki Coloring - Creative Musical Art Experience",
                "description": "Explore Spranki's creative coloring experience. Combine music and art in this interactive coloring activity. Perfect for creative minds!",
                "keywords": ["spranki coloring", "sprankiy art", "sprankis coloring", "music coloring", "interactive art", "creative music activity"],
                "og_image": "/static/images/spranki-coloring.jpg"
            },
            "about": {
                "title": "About Spranki - Our Story and Mission",
                "description": "Learn about Spranki's mission to combine music, gaming, and education. Discover how we create interactive experiences for all ages.",
                "keywords": ["about spranki", "sprankį story", "sprankiy mission", "spranki history", "interactive music education"],
                "og_image": "/static/images/spranki-about.jpg"
            }
        }
