import os
import glob

# Caminho para o diretório onde ficam as migrações
migration_dirs = glob.glob("./*/migrations")

for dir in migration_dirs:
    for migration_file in os.listdir(dir):
        if migration_file != "__init__.py" and migration_file.endswith(".py"):
            os.remove(os.path.join(dir, migration_file))
            print(f"Deleted {migration_file} from {dir}")
