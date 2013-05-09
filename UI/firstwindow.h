#ifndef FIRSTWINDOW_H
#define FIRSTWINDOW_H

#include <QWidget>
#include "upload.h"
namespace Ui {
class FirstWindow;
}

class FirstWindow : public QWidget
{
    Q_OBJECT
    
public:
    upload *up;
    explicit FirstWindow(QWidget *parent = 0);
    ~FirstWindow();


public slots:
    void next();
    
private:
    Ui::FirstWindow *ui;

 signals:
    void movenext();
};

#endif // FIRSTWINDOW_H
