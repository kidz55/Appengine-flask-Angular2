import { FrontPictarinePage } from './app.po';

describe('front-pictarine App', () => {
  let page: FrontPictarinePage;

  beforeEach(() => {
    page = new FrontPictarinePage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
