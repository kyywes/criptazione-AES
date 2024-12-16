import fs from 'fs-extra';
import inquirer from 'inquirer';
import path from 'path';

async function runWizard() {
  console.log('Benvenuto nel wizard di EncryptorApp!\n');

  // Passaggio 1: Chiedi il nome dell'utente
  const { username } = await inquirer.prompt([
    {
      type: 'input',
      name: 'username',
      message: 'Inserisci il tuo nome:',
    },
  ]);

  // Passaggio 2: Chiedi il percorso di installazione
  const { installPath } = await inquirer.prompt([
    {
      type: 'input',
      name: 'installPath',
      message: 'Inserisci il percorso di installazione:',
      default: path.join('C:\\Users', process.env.USERNAME, 'EncryptorApp'),
    },
  ]);

  // Passaggio 3: Conferma l'installazione
  const { confirmInstall } = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'confirmInstall',
      message: `Confermi l'installazione in ${installPath}?`,
      default: true,
    },
  ]);

  if (confirmInstall) {
    try {
      const sourceFile = path.join(process.cwd(), 'EncryptorApp.exe');
      const targetFile = path.join(installPath, 'EncryptorApp.exe');

      fs.ensureDirSync(installPath);
      fs.copyFileSync(sourceFile, targetFile);

      console.log(`Installazione completata con successo in: ${installPath}`);
    } catch (error) {
      console.error('Errore durante l’installazione:', error.message);
    }
  } else {
    console.log('Installazione annullata.');
  }
}

runWizard();
